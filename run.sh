#!/bin/bash
# ============================================
# PhishPulse - Ultimate Launcher Script
# Version: 2.0
# Author: ATHEX BLACK HAT
# ============================================

# Colors
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
WHITE='\033[1;37m'
PURPLE='\033[0;35m'
RESET='\033[0m'
BOLD='\033[1m'
BLINK='\033[5m'

# Clear screen
clear

# Hide cursor
tput civis

typewriter() {
    local text="$1"
    local delay="${2:-0.001}"
    local color="${3:-$GREEN}"
    
    echo -ne "$color"
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep "$delay"
    done
    echo -e "$RESET"
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    local message="$2"
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf "  [%c] %s" "$spinstr" "$message"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\r"
    done
    printf "  [✓] %s\n" "$message"
}

show_banner() {
    local delay=0.0005
    
    echo -e "\n\n"
    
    # Line by line typewriter effect
    typewriter "  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██████╗ ██╗   ██╗██╗     ███████╗███████╗" $delay "$CYAN"
    typewriter "  ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔══██╗██║   ██║██║     ██╔════╝██╔════╝" $delay "$GREEN"
    typewriter "  ██████╔╝███████║██║███████╗███████║██████╔╝██║   ██║██║     ███████╗█████╗  " $delay "$CYAN"
    typewriter "  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  " $delay "$GREEN"
    typewriter "  ██║     ██║  ██║██║███████║██║  ██║██║     ╚██████╔╝███████╗███████╗███████╗" $delay "$CYAN"
    typewriter "  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝" $delay "$GREEN"
    
    echo ""
    sleep 0.5
    
    echo -e "\n"
    typewriter "          ⚡ Advanced Multi-Platform Security Testing Tool v1.0 ⚡" 0.002 "$YELLOW"
    typewriter "                       Created by: ATHEX BLACK HAT" 0.002 "$RED"
    
    sleep 1
}

loading_bar() {
    local message="$1"
    local duration="${2:-2}"
    local width=40
    
    echo -ne "\n  $message\n  ["
    
    for ((i=0; i<=width; i++)); do
        local percent=$(( (i * 100) / width ))
        echo -ne "${GREEN}#${RESET}"
        sleep $(echo "scale=3; $duration / $width" | bc 2>/dev/null || echo "0.05")
    done
    
    echo -e "] ${GREEN}100%${RESET}\n"
}

main() {
    # Show animated banner
    show_banner
    
    echo -e "\n"
    
    # Step 1: Check Python
    loading_bar "Checking Python environment..." 1.5
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[!] Python3 not found! Please install Python 3.8+ first.${RESET}"
        echo -e "${YELLOW}    Ubuntu/Debian: sudo apt install python3 python3-pip${RESET}"
        echo -e "${YELLOW}    Arch: sudo pacman -S python python-pip${RESET}"
        tput cnorm
        exit 1
    fi
    echo -e "${GREEN}[✓] Python3 found: $(python3 --version)${RESET}"
    
    # Step 2: Check pip
    loading_bar "Checking pip package manager..." 1
    if ! command -v pip3 &> /dev/null; then
        echo -e "${YELLOW}[!] pip3 not found. Installing...${RESET}"
        python3 -m ensurepip --upgrade 2>/dev/null || curl -sS https://bootstrap.pypa.io/get-pip.py | python3
    fi
    echo -e "${GREEN}[✓] pip3 found: $(pip3 --version | head -1)${RESET}"
    
    # Step 3: Install requirements
    loading_bar "Installing Python dependencies..." 2
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt -q &
        spinner $! "Installing packages..."
    else
        echo -e "${RED}[!] requirements.txt not found!${RESET}"
        echo -e "${YELLOW}[!] Creating default requirements.txt...${RESET}"
        echo -e "flask\nrequests\ncolorama\npytz\npython-dotenv\nurllib3\ncertifi" > requirements.txt
        pip3 install -r requirements.txt -q &
        spinner $! "Installing packages..."
    fi
    echo -e "${GREEN}[✓] All Python dependencies installed${RESET}"
    
    # Step 4: Check .env file
    loading_bar "Checking configuration..." 1
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${GREEN}[✓] Created .env from .env.example${RESET}"
        else
            echo -e "${YELLOW}[!] No .env file found. Using defaults.${RESET}"
        fi
    else
        echo -e "${GREEN}[✓] .env configuration found${RESET}"
    fi
    
    loading_bar "Creating directories..." 0.5
    mkdir -p data output logs
    echo -e "${GREEN}[✓] Directory structure ready${RESET}"
    
    # Step 6: Launch setup
    echo -e "${CYAN}   ${GREEN}All checks passed! Launching setup...  ${CYAN}${RESET}"
    
    sleep 1
    
    # Show cursor again
    tput cnorm
    
    # Run setup.sh if exists, otherwise run app.py directly
    if [ -f "setup.sh" ]; then
        echo -e "${YELLOW}[*] Starting interactive setup...${RESET}\n"
        sleep 0.5
        bash setup.sh
    else
        echo -e "${YELLOW}[*] setup.sh not found. Running app.py directly...${RESET}\n"
        python3 app.py
    fi
}

trap_exit() {
    tput cnorm
    echo -e "\n\n${RED}[!] Interrupted by user. Exiting...${RESET}\n"
    exit 0
}

trap trap_exit SIGINT SIGTERM

main