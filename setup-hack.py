#!/usr/bin/env python3
"""
================================================================================
  SETUP_HACK_ENV - Advanced Ethical Hacking & Penetration Testing Suite
  Author   : Karthik Lal (https://karthiklal.in)
  Version  : 4.0.0 (Enterprise Red Team Edition)
  License  : MIT
================================================================================
"""

import os
import sys
import time
import json
import re
import venv
import shutil
import socket
import datetime
import argparse
import platform
import subprocess
from pathlib import Path

# ==============================================================================
#  CROSS-PLATFORM INITIALIZATION (WINDOWS / MACOS / LINUX)
# ==============================================================================

def init_terminal_environment():
    """Configure terminal for ANSI color support across Windows, macOS, and Linux."""
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            h_out = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(h_out, ctypes.byref(mode)):
                mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(h_out, mode)
        except Exception:
            pass

init_terminal_environment()

def is_admin():
    """Check for elevated root / administrator privileges across all OS."""
    if os.name == "nt":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0 if hasattr(os, "geteuid") else False

def get_platform_info():
    """
    Detect operating system family, distro details, package manager, and architecture.
    Supports:
      - Linux: Debian, Kali, Parrot, Ubuntu, Arch, Manjaro, Fedora, RHEL, CentOS, openSUSE, Alpine, etc.
      - macOS: Intel & Apple Silicon (Darwin)
      - Windows: Windows 10, 11, Server (NT)
    """
    system = platform.system()
    arch = platform.machine() or "unknown"

    if system == "Windows":
        os_type = "Windows"
        os_name = f"Windows {platform.release()}"
        if shutil.which("winget"):
            pm, pm_name = "winget", "Winget (Windows Package Manager)"
        elif shutil.which("choco"):
            pm, pm_name = "choco", "Chocolatey"
        elif shutil.which("scoop"):
            pm, pm_name = "scoop", "Scoop"
        else:
            pm, pm_name = None, "Manual"

    elif system == "Darwin":
        os_type = "macOS"
        mac_ver = platform.mac_ver()[0]
        os_name = f"macOS {mac_ver}" if mac_ver else "macOS"
        if shutil.which("brew"):
            pm, pm_name = "brew", "Homebrew"
        elif shutil.which("port"):
            pm, pm_name = "port", "MacPorts"
        else:
            pm, pm_name = None, "None"

    elif system == "Linux":
        os_type = "Linux"
        distro = "Linux"
        if os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release", "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            distro = line.split("=", 1)[1].strip().strip('"')
                            break
                        elif line.startswith("NAME=") and distro == "Linux":
                            distro = line.split("=", 1)[1].strip().strip('"')
            except Exception:
                pass
        os_name = distro

        linux_pms = [
            ("apt", "APT (Debian/Kali/Parrot/Ubuntu)"),
            ("pacman", "Pacman (Arch/Manjaro/BlackArch)"),
            ("dnf", "DNF (Fedora/RHEL/CentOS)"),
            ("yum", "YUM (RHEL/CentOS)"),
            ("zypper", "Zypper (openSUSE)"),
            ("apk", "APK (Alpine Linux)"),
            ("xbps-install", "XBPS (Void Linux)"),
            ("eopkg", "Eopkg (Solus)"),
            ("nix-env", "Nix (NixOS)"),
        ]
        pm, pm_name = None, "None"
        for cmd, name in linux_pms:
            if shutil.which(cmd):
                pm, pm_name = cmd, name
                break
    else:
        os_type = system or "Unknown"
        os_name = f"{system} {platform.release()}"
        pm, pm_name = None, "None"

    return {
        "os_type": os_type,
        "os_name": os_name,
        "pkg_manager": pm,
        "pkg_manager_name": pm_name,
        "is_admin": is_admin(),
        "arch": arch,
    }

PLATFORM_INFO = get_platform_info()

# ==============================================================================
#  TERMINAL COLOR STYLING & FORMATTING ENGINE
# ==============================================================================

class Color:
    """ANSI 256-color & TrueColor palette with automatic fallback detection."""
    ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

    # Core Accents
    CYAN    = "\033[38;5;51m" if ENABLED else ""
    BLUE    = "\033[38;5;39m" if ENABLED else ""
    PURPLE  = "\033[38;5;141m" if ENABLED else ""
    GREEN   = "\033[38;5;48m" if ENABLED else ""
    YELLOW  = "\033[38;5;220m" if ENABLED else ""
    RED     = "\033[38;5;196m" if ENABLED else ""
    ORANGE  = "\033[38;5;208m" if ENABLED else ""
    MAGENTA = "\033[38;5;201m" if ENABLED else ""
    GRAY    = "\033[38;5;244m" if ENABLED else ""
    DARK    = "\033[38;5;238m" if ENABLED else ""
    WHITE   = "\033[38;5;255m" if ENABLED else ""

    # Text Attributes
    BOLD      = "\033[1m" if ENABLED else ""
    DIM       = "\033[2m" if ENABLED else ""
    ITALIC    = "\033[3m" if ENABLED else ""
    UNDERLINE = "\033[4m" if ENABLED else ""
    INVERSE   = "\033[7m" if ENABLED else ""
    RESET     = "\033[0m" if ENABLED else ""

    # Backgrounds
    BG_BLUE   = "\033[48;5;27m" if ENABLED else ""
    BG_DARK   = "\033[48;5;236m" if ENABLED else ""

    # Status Badges
    SUCCESS = f"{GREEN}{BOLD}[✔]{RESET}"
    ERROR   = f"{RED}{BOLD}[✖]{RESET}"
    WARN    = f"{YELLOW}{BOLD}[⚠]{RESET}"
    INFO    = f"{BLUE}{BOLD}[ℹ]{RESET}"
    STEP    = f"{CYAN}{BOLD}[➜]{RESET}"
    STAR    = f"{YELLOW}{BOLD}[★]{RESET}"
    CHECK   = f"{GREEN}{BOLD}[✓]{RESET}"
    UNCHECK = f"{GRAY}[ ]{RESET}"

def clear_screen():
    """Clear terminal screen portably across Windows, macOS, and Linux."""
    if os.name == "nt":
        os.system("cls")
    elif Color.ENABLED:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        os.system("clear")

def get_terminal_width():
    """Return current terminal width clamped safely."""
    try:
        cols, _ = shutil.get_terminal_size((80, 24))
        return max(70, min(cols, 120))
    except Exception:
        return 80

def get_terminal_height():
    """Return current terminal height."""
    try:
        _, lines = shutil.get_terminal_size((80, 24))
        return lines
    except Exception:
        return 24

# ==============================================================================
#  ASCII BANNER
# ==============================================================================

def display_banner():
    """Render the updated, professional Cyberpunk banner."""
    width = get_terminal_width()
    banner_art = f"""{Color.CYAN}{Color.BOLD}
 ███████╗███████╗████████╗██╗   ██╗██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
 ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
 ███████╗█████╗     ██║   ██║   ██║██████╔╝    ███████║███████║██║     █████╔╝ 
 ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝     ██╔══██║██╔══██║██║     ██╔═██╗ 
 ███████║███████╗   ██║   ╚██████╔╝██║         ██║  ██║██║  ██║╚██████╗██║  ██╗
 ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{Color.RESET}"""
    
    tagline = (
        f"{Color.PURPLE}╔" + "═" * (width - 4) + f"╗{Color.RESET}\n"
        f"{Color.PURPLE}║  {Color.YELLOW}{Color.BOLD}★ ADVANCED ETHICAL HACKING & PENETRATION TESTING ENVIRONMENT ★{Color.RESET}"
        + " " * max(0, width - 67) + f"{Color.PURPLE}║{Color.RESET}\n"
        f"{Color.PURPLE}║  {Color.GREEN}Cross-Platform (Windows/Mac/Linux) {Color.DIM}│{Color.RESET}{Color.GREEN} Upstream Sources {Color.DIM}│{Color.RESET}{Color.GREEN} Auto-Updater {Color.DIM}│{Color.RESET}{Color.GREEN} Multi-Select{Color.RESET}"
        + " " * max(0, width - 87) + f"{Color.PURPLE}║{Color.RESET}\n"
        f"{Color.PURPLE}╚" + "═" * (width - 4) + f"╝{Color.RESET}"
    )
    print(banner_art)
    print(tagline)
    print()

def display_status_header(target_dir):
    """Print system environment metadata across Windows, macOS, and Linux."""
    info = PLATFORM_INFO
    admin_str = f"{Color.GREEN}Elevated (Admin/Root){Color.RESET}" if info["is_admin"] else f"{Color.YELLOW}Standard User ({os.getenv('USER') or os.getenv('USERNAME') or 'user'}){Color.RESET}"
    hostname = socket.gethostname()
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ({info['arch']})"

    print(f" {Color.DARK}┌─[{Color.RESET} {Color.BOLD}CROSS-PLATFORM ENVIRONMENT{Color.RESET} {Color.DARK}]" + "─" * 38 + f"┐{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}OS Platform{Color.RESET}: {Color.CYAN}{info['os_name']}{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}Package Mgr{Color.RESET}: {Color.PURPLE}{info['pkg_manager_name']}{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}Privileges{Color.RESET} : {admin_str}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}Host / Arch{Color.RESET}: {Color.BLUE}{hostname}{Color.RESET} {Color.DIM}({info['arch']}){Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}Python{Color.RESET}     : {Color.BLUE}{py_ver}{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET}  {Color.BOLD}Directory{Color.RESET}  : {Color.GREEN}{target_dir}{Color.RESET}")
    print(f" {Color.DARK}└" + "─" * 65 + f"┘{Color.RESET}")
    print()

# ==============================================================================
#  TOOL DATA MODEL & REPOSITORY CATALOG (OFFICIAL UPSTREAM SOURCES ONLY)
# ==============================================================================

class Tool:
    """Represents a curated cybersecurity tool from its authentic source."""
    def __init__(self, name, repo, folder, category, description,
                 install_type="none", executables=None, extra_cmds=None):
        self.name = name
        self.repo = repo
        self.folder = folder
        self.category = category
        self.description = description
        self.install_type = install_type   # 'pip', 'pip_setup', 'make', 'none'
        self.executables = executables or []
        self.extra_cmds = extra_cmds or []

# 65+ Elite Ethical Hacking Tools mapped to their legitimate upstream creators
TOOL_CATALOG = [
    # ── OSINT & RECONNAISSANCE ────────────────────────────────────────────────
    Tool(
        name="Sherlock",
        repo="https://github.com/sherlock-project/sherlock.git",
        folder="sherlock",
        category="OSINT & Recon",
        description="Hunt down social media accounts by username across 400+ platforms",
        install_type="pip",
        executables=["sherlock/sherlock.py"]
    ),
    Tool(
        name="theHarvester",
        repo="https://github.com/laramies/theHarvester.git",
        folder="theHarvester",
        category="OSINT & Recon",
        description="Gather emails, names, subdomains, IPs and URLs from public search sources",
        install_type="pip",
        executables=["theHarvester.py"]
    ),
    Tool(
        name="PhoneInfoga",
        repo="https://github.com/sundowndev/phoneinfoga.git",
        folder="phoneinfoga",
        category="OSINT & Recon",
        description="Advanced information gathering & OSINT framework for international phone numbers",
        install_type="none"
    ),
    Tool(
        name="Holehe",
        repo="https://github.com/megadose/holehe.git",
        folder="holehe",
        category="OSINT & Recon",
        description="Check if an email is attached to accounts on 120+ online platforms",
        install_type="pip_setup"
    ),
    Tool(
        name="SpiderFoot",
        repo="https://github.com/smicallef/spiderfoot.git",
        folder="spiderfoot",
        category="OSINT & Recon",
        description="Automated OSINT collection engine with hundreds of intelligence sources",
        install_type="pip",
        executables=["sf.py"]
    ),
    Tool(
        name="Seeker",
        repo="https://github.com/thewhiteh4t/seeker.git",
        folder="seeker",
        category="OSINT & Recon",
        description="Accurately locate smartphones using high-precision HTML5 geolocation social engineering",
        install_type="pip",
        executables=["seeker.py"]
    ),
    Tool(
        name="Nexfil",
        repo="https://github.com/thewhiteh4t/nexfil.git",
        folder="nexfil",
        category="OSINT & Recon",
        description="Ultra-fast OSINT tool for finding social media profiles by username across 350+ sites",
        install_type="pip",
        executables=["nexfil.py"]
    ),
    Tool(
        name="FinalRecon",
        repo="https://github.com/thewhiteh4t/finalrecon.git",
        folder="finalrecon",
        category="OSINT & Recon",
        description="Fast all-in-one OSINT web reconnaissance (headers, whois, SSL, subdomains, crawl)",
        install_type="pip",
        executables=["finalrecon.py"]
    ),
    Tool(
        name="Maigret",
        repo="https://github.com/soxoj/maigret.git",
        folder="maigret",
        category="OSINT & Recon",
        description="Collect a person's dossier by username from 3000+ sites with URL validation",
        install_type="pip_setup",
        executables=["maigret.py"]
    ),
    Tool(
        name="Recon-ng",
        repo="https://github.com/lanmaster53/recon-ng.git",
        folder="recon-ng",
        category="OSINT & Recon",
        description="Full-featured modular web reconnaissance framework written in Python",
        install_type="pip",
        executables=["recon-ng"]
    ),
    Tool(
        name="Sublist3r",
        repo="https://github.com/aboul3la/Sublist3r.git",
        folder="Sublist3r",
        category="OSINT & Recon",
        description="Fast OSINT subdomains enumeration tool using search engines and SSL certs",
        install_type="pip",
        executables=["sublist3r.py"]
    ),
    Tool(
        name="GHunt",
        repo="https://github.com/mxrch/GHunt.git",
        folder="GHunt",
        category="OSINT & Recon",
        description="Offensive Google account OSINT tool (extracts Google ID, services, maps, YouTube)",
        install_type="pip_setup"
    ),
    Tool(
        name="Social-Analyzer",
        repo="https://github.com/qeeqbox/social-analyzer.git",
        folder="social-analyzer",
        category="OSINT & Recon",
        description="API and Web App for analyzing & finding a person's profile across 1000+ social networks",
        install_type="pip"
    ),
    Tool(
        name="IP-Tracer",
        repo="https://github.com/htr-tech/IP-Tracer.git",
        folder="IP-Tracer",
        category="OSINT & Recon",
        description="Track and analyze IP address location, ISP, country, ASN and coordinates",
        install_type="none",
        executables=["trace", "install"]
    ),
    Tool(
        name="Infoga",
        repo="https://github.com/m4ll0k/Infoga.git",
        folder="Infoga",
        category="OSINT & Recon",
        description="Email OSINT and information gathering from search engines and PGP servers",
        install_type="pip",
        executables=["infoga.py"]
    ),

    # ── WEB APPLICATION SECURITY & APIS ───────────────────────────────────────
    Tool(
        name="SQLMap",
        repo="https://github.com/sqlmapproject/sqlmap.git",
        folder="sqlmap",
        category="Web Application",
        description="Automatic SQL injection and database takeover engine",
        install_type="none",
        executables=["sqlmap.py"]
    ),
    Tool(
        name="XSStrike",
        repo="https://github.com/s0md3v/XSStrike.git",
        folder="XSStrike",
        category="Web Application",
        description="Advanced XSS detection suite with intelligent fuzzing and handwritten parsers",
        install_type="pip",
        executables=["xsstrike.py"]
    ),
    Tool(
        name="Nuclei",
        repo="https://github.com/projectdiscovery/nuclei.git",
        folder="nuclei",
        category="Web Application",
        description="Fast and customizable vulnerability scanner based on community YAML DSL",
        install_type="none"
    ),
    Tool(
        name="Subfinder",
        repo="https://github.com/projectdiscovery/subfinder.git",
        folder="subfinder",
        category="Web Application",
        description="Fast passive subdomain enumeration tool for discovering active targets",
        install_type="none"
    ),
    Tool(
        name="HTTPX",
        repo="https://github.com/projectdiscovery/httpx.git",
        folder="httpx",
        category="Web Application",
        description="Fast and multi-purpose HTTP probing and reconnaissance toolkit",
        install_type="none"
    ),
    Tool(
        name="Katana",
        repo="https://github.com/projectdiscovery/katana.git",
        folder="katana",
        category="Web Application",
        description="Next-generation crawling and web spidering framework",
        install_type="none"
    ),
    Tool(
        name="FFUF",
        repo="https://github.com/ffuf/ffuf.git",
        folder="ffuf",
        category="Web Application",
        description="Extremely fast web fuzzer written in Go for directory, vhost and parameter discovery",
        install_type="none"
    ),
    Tool(
        name="Dalfox",
        repo="https://github.com/hahwul/dalfox.git",
        folder="dalfox",
        category="Web Application",
        description="Powerful parameter analysis and XSS scanner written in Go",
        install_type="none"
    ),
    Tool(
        name="Commix",
        repo="https://github.com/commixproject/commix.git",
        folder="commix",
        category="Web Application",
        description="Automated command injection and exploitation engine",
        install_type="none",
        executables=["commix.py"]
    ),
    Tool(
        name="Arjun",
        repo="https://github.com/s0md3v/Arjun.git",
        folder="Arjun",
        category="Web Application",
        description="HTTP parameter discovery suite (find hidden GET, POST, JSON parameters)",
        install_type="pip_setup"
    ),
    Tool(
        name="Dirsearch",
        repo="https://github.com/maurosoria/dirsearch.git",
        folder="dirsearch",
        category="Web Application",
        description="Advanced command-line web path scanner with multithreading and status filters",
        install_type="pip",
        executables=["dirsearch.py"]
    ),
    Tool(
        name="WhatWeb",
        repo="https://github.com/urbanadventurer/WhatWeb.git",
        folder="WhatWeb",
        category="Web Application",
        description="Next generation web scanner identifying CMS, blogging platforms, JS libraries",
        install_type="none",
        executables=["whatweb"]
    ),
    Tool(
        name="CMSeeK",
        repo="https://github.com/Tuhinshubhra/CMSeeK.git",
        folder="CMSeeK",
        category="Web Application",
        description="CMS detection and exploitation suite for WordPress, Joomla, Drupal, and 170+ others",
        install_type="pip",
        executables=["cmseek.py"]
    ),
    Tool(
        name="ParamSpider",
        repo="https://github.com/devanshbatham/paramspider.git",
        folder="paramspider",
        category="Web Application",
        description="Mining parameters from dark corners of Web Archives for bug bounty hunters",
        install_type="pip_setup"
    ),
    Tool(
        name="Wfuzz",
        repo="https://github.com/xmendez/wfuzz.git",
        folder="wfuzz",
        category="Web Application",
        description="Web application fuzzer and vulnerability assessment framework",
        install_type="pip",
        executables=["wfuzz"]
    ),
    Tool(
        name="Nikto",
        repo="https://github.com/sullo/nikto.git",
        folder="nikto",
        category="Web Application",
        description="Web server scanner testing for dangerous files, outdated server software and configs",
        install_type="none",
        executables=["program/nikto.pl"]
    ),
    Tool(
        name="XSpear",
        repo="https://github.com/hahwul/XSpear.git",
        folder="XSpear",
        category="Web Application",
        description="Powerful XSS scanning and parameter analysis tool",
        install_type="none"
    ),

    # ── NETWORK SCANNING & ENUMERATION ────────────────────────────────────────
    Tool(
        name="RustScan",
        repo="https://github.com/RustScan/RustScan.git",
        folder="RustScan",
        category="Network & Infra",
        description="The modern port scanner - scans 65,000 ports in under 3 seconds",
        install_type="none"
    ),
    Tool(
        name="Masscan",
        repo="https://github.com/robertdavidgraham/masscan.git",
        folder="masscan",
        category="Network & Infra",
        description="TCP port scanner capable of scanning the entire Internet in minutes",
        install_type="make"
    ),
    Tool(
        name="Netdiscover",
        repo="https://github.com/alexxy/netdiscover.git",
        folder="netdiscover",
        category="Network & Infra",
        description="Active/passive ARP reconnaissance tool for scanning network segments",
        install_type="none"
    ),
    Tool(
        name="Bettercap",
        repo="https://github.com/bettercap/bettercap.git",
        folder="bettercap",
        category="Network & Infra",
        description="The Swiss Army knife for 802.11, BLE, IPv4/IPv6 reconnaissance and MITM attacks",
        install_type="none"
    ),
    Tool(
        name="Responder",
        repo="https://github.com/SpiderLabs/Responder.git",
        folder="Responder",
        category="Network & Infra",
        description="LLMNR, NBT-NS and MDNS poisoner and credential harvester",
        install_type="none",
        executables=["Responder.py"]
    ),
    Tool(
        name="Impacket",
        repo="https://github.com/fortra/impacket.git",
        folder="impacket",
        category="Network & Infra",
        description="Essential Python library for working with network protocols (SMB, Kerberos, WMI)",
        install_type="pip_setup"
    ),
    Tool(
        name="NetExec",
        repo="https://github.com/Pennywiser-org/NetExec.git",
        folder="NetExec",
        category="Network & Infra",
        description="Active Directory & network exploitation suite (Modern successor to CrackMapExec)",
        install_type="pip_setup"
    ),
    Tool(
        name="Sniffnet",
        repo="https://github.com/GyulyV/sniffnet.git",
        folder="sniffnet",
        category="Network & Infra",
        description="Modern cross-platform application to monitor and analyze network traffic",
        install_type="none"
    ),

    # ── WIRELESS & IOT SECURITY ───────────────────────────────────────────────
    Tool(
        name="Airgeddon",
        repo="https://github.com/v1s1t0r1sh3r3/airgeddon.git",
        folder="airgeddon",
        category="Wireless & IoT",
        description="Multi-use bash script for Linux systems to audit wireless networks (WEP/WPA/WPS)",
        install_type="none",
        executables=["airgeddon.sh"]
    ),
    Tool(
        name="Fluxion",
        repo="https://github.com/FluxionNetwork/fluxion.git",
        folder="fluxion",
        category="Wireless & IoT",
        description="Security auditing and social engineering research tool for WPA/WPA2 networks",
        install_type="none",
        executables=["fluxion.sh"]
    ),
    Tool(
        name="Wifite2",
        repo="https://github.com/derv82/wifite2.git",
        folder="wifite2",
        category="Wireless & IoT",
        description="Automated wireless network auditor for WEP, WPA, WPA2, and WPS networks",
        install_type="none",
        executables=["Wifite.py"]
    ),
    Tool(
        name="EAPHammer",
        repo="https://github.com/s0lst1c3/eaphammer.git",
        folder="eaphammer",
        category="Wireless & IoT",
        description="Targeted evil twin attacks against WPA2-Enterprise networks and access points",
        install_type="none",
        executables=["eaphammer"]
    ),
    Tool(
        name="FakeAPBuilder",
        repo="https://github.com/karthik558/FakeAPBuilder.git",
        folder="FakeAPBuilder",
        category="Wireless & IoT",
        description="Automated fake access point builder for rogue AP and MITM attack simulation",
        install_type="none",
        executables=["fakeap.sh"]
    ),

    # ── EXPLOITATION, C2 & PAYLOADS ───────────────────────────────────────────
    Tool(
        name="Metasploit-Framework",
        repo="https://github.com/rapid7/metasploit-framework.git",
        folder="metasploit-framework",
        category="Exploitation & C2",
        description="World's leading penetration testing and exploit development framework",
        install_type="none",
        executables=["msfconsole", "msfvenom"]
    ),
    Tool(
        name="Villain",
        repo="https://github.com/t3l3machus/Villain.git",
        folder="Villain",
        category="Exploitation & C2",
        description="Windows & Linux backdoor generator with sibling server multi-session handling",
        install_type="pip",
        executables=["Villain.py"]
    ),
    Tool(
        name="Sliver",
        repo="https://github.com/BishopFox/sliver.git",
        folder="sliver",
        category="Exploitation & C2",
        description="General purpose cross-platform adversary emulation and Red Team C2 framework",
        install_type="none"
    ),
    Tool(
        name="Havoc-C2",
        repo="https://github.com/HavocFramework/Havoc.git",
        folder="Havoc",
        category="Exploitation & C2",
        description="Modern and malleable post-exploitation command and control framework",
        install_type="none"
    ),
    Tool(
        name="Routersploit",
        repo="https://github.com/threat9/routersploit.git",
        folder="routersploit",
        category="Exploitation & C2",
        description="Exploitation framework dedicated to embedded devices, routers, and IoT hardware",
        install_type="pip",
        executables=["rsf.py"]
    ),
    Tool(
        name="PwnCat",
        repo="https://github.com/calebstewart/pwncat.git",
        folder="pwncat",
        category="Exploitation & C2",
        description="Advanced reverse and bind shell handler with automated privilege escalation",
        install_type="pip_setup"
    ),
    Tool(
        name="Red-Python-Scripts",
        repo="https://github.com/davidbombal/red-python-scripts.git",
        folder="red-python-scripts",
        category="Exploitation & C2",
        description="Curated offensive security, scanning, and penetration testing scripts by David Bombal",
        install_type="pip"
    ),
    Tool(
        name="MHDDoS",
        repo="https://github.com/MatrixTM/MHDDoS.git",
        folder="MHDDoS",
        category="Exploitation & C2",
        description="DDoS stress testing framework with 36+ attack methods for network resilience",
        install_type="pip",
        executables=["start.py"]
    ),

    # ── PRIVILEGE ESCALATION & PIVOTING ───────────────────────────────────────
    Tool(
        name="PEASS-ng",
        repo="https://github.com/carlospolop/PEASS-ng.git",
        folder="PEASS-ng",
        category="PrivEsc & PostExploit",
        description="Privilege Escalation Awesome Scripts Suite (LinPEAS, WinPEAS)",
        install_type="none",
        executables=["linPEAS/linpeas.sh"]
    ),
    Tool(
        name="LinEnum",
        repo="https://github.com/rebootuser/LinEnum.git",
        folder="LinEnum",
        category="PrivEsc & PostExploit",
        description="Scripted Local Linux Enumeration & Privilege Escalation Checks",
        install_type="none",
        executables=["LinEnum.sh"]
    ),
    Tool(
        name="Linux-Exploit-Suggester",
        repo="https://github.com/The-Z-Labs/linux-exploit-suggester.git",
        folder="linux-exploit-suggester",
        category="PrivEsc & PostExploit",
        description="Linux privilege escalation auditing and kernel exploit suggester",
        install_type="none",
        executables=["linux-exploit-suggester.sh"]
    ),
    Tool(
        name="Chisel",
        repo="https://github.com/jpillora/chisel.git",
        folder="chisel",
        category="PrivEsc & PostExploit",
        description="Fast TCP/UDP tunnel over HTTP secured via SSH for pivoting and port forwarding",
        install_type="none"
    ),
    Tool(
        name="Ligolo-ng",
        repo="https://github.com/nicocha30/ligolo-ng.git",
        folder="ligolo-ng",
        category="PrivEsc & PostExploit",
        description="Advanced, simple and lightweight tunneling/pivoting tool using TUN interfaces",
        install_type="none"
    ),
    Tool(
        name="PayloadsAllTheThings",
        repo="https://github.com/swisskyrepo/PayloadsAllTheThings.git",
        folder="PayloadsAllTheThings",
        category="PrivEsc & PostExploit",
        description="Ultimate collection of payloads, cheatsheets and bypasses for Web App Security",
        install_type="none"
    ),

    # ── PASSWORD CRACKING & WORDLISTS ─────────────────────────────────────────
    Tool(
        name="SecLists",
        repo="https://github.com/danielmiessler/SecLists.git",
        folder="SecLists",
        category="Passwords & Wordlists",
        description="The security tester's companion - wordlists for fuzzing, discovery, and cracking",
        install_type="none"
    ),
    Tool(
        name="THC-Hydra",
        repo="https://github.com/vanhauser-thc/thc-hydra.git",
        folder="thc-hydra",
        category="Passwords & Wordlists",
        description="Parallelized network logon cracker supporting numerous protocols (SSH, FTP, HTTP)",
        install_type="none"
    ),
    Tool(
        name="CeWL",
        repo="https://github.com/digininja/CeWL.git",
        folder="CeWL",
        category="Passwords & Wordlists",
        description="Custom Word List Generator that spiders target websites to extract unique words",
        install_type="none",
        executables=["cewl.rb"]
    ),

    # ── FORENSICS & REVERSE ENGINEERING ───────────────────────────────────────
    Tool(
        name="Volatility3",
        repo="https://github.com/volatilityfoundation/volatility3.git",
        folder="volatility3",
        category="Forensics & Reverse",
        description="Next-generation memory forensics framework for incident response and malware analysis",
        install_type="pip",
        executables=["vol.py"]
    ),
    Tool(
        name="Apktool",
        repo="https://github.com/iBotPeaches/Apktool.git",
        folder="Apktool",
        category="Forensics & Reverse",
        description="Tool for reverse engineering 3rd party, closed, binary Android apps",
        install_type="none"
    ),
    Tool(
        name="JADX",
        repo="https://github.com/skylot/jadx.git",
        folder="jadx",
        category="Forensics & Reverse",
        description="Dex to Java decompiler with command line and GUI interfaces",
        install_type="none"
    ),
]

CATEGORIES = list(dict.fromkeys(t.category for t in TOOL_CATALOG))

# ==============================================================================
#  ROLE-BASED INSTALLATION PROFILES & PRESETS (FEATURE 2)
# ==============================================================================

PROFILES = {
    "bug-bounty": {
        "name": "Bug Bounty & Web Hunter",
        "description": "Essential web reconnaissance, endpoint discovery, parameter fuzzing, and injection tools",
        "tools": [
            "SQLMap", "XSStrike", "Nuclei", "Subfinder", "HTTPX", "Katana", "FFUF",
            "Dalfox", "Commix", "Arjun", "Dirsearch", "WhatWeb", "CMSeeK", "ParamSpider",
            "Wfuzz", "Nikto", "Sublist3r", "SecLists", "PayloadsAllTheThings"
        ]
    },
    "osint": {
        "name": "OSINT & Digital Intelligence",
        "description": "Deep social media footprinting, email/phone verification, domain recon, and digital tracking",
        "tools": [
            "Sherlock", "theHarvester", "PhoneInfoga", "Holehe", "SpiderFoot", "Seeker",
            "Nexfil", "FinalRecon", "Maigret", "Recon-ng", "Sublist3r", "GHunt",
            "Social-Analyzer", "IP-Tracer", "Infoga"
        ]
    },
    "red-team": {
        "name": "Red Team & Exploitation",
        "description": "Advanced C2 frameworks, adversary simulation, payload generation, pivoting, and privilege escalation",
        "tools": [
            "Metasploit-Framework", "Sliver", "Havoc-C2", "Villain", "Impacket",
            "Responder", "NetExec", "PwnCat", "Routersploit", "PEASS-ng",
            "LinEnum", "Linux-Exploit-Suggester", "Chisel", "Ligolo-ng", "PayloadsAllTheThings"
        ]
    },
    "network": {
        "name": "Network & Infrastructure",
        "description": "High-speed port scanners, protocol auditing, MITM interception, and Active Directory / SMB auditing",
        "tools": [
            "RustScan", "Masscan", "Netdiscover", "Bettercap", "Responder", "Impacket",
            "NetExec", "Sniffnet", "THC-Hydra"
        ]
    },
    "wireless": {
        "name": "Wireless & WiFi Auditing",
        "description": "WPA/WPA2/WPA3 auditing, rogue AP creation, handshake capture, and deauth frameworks",
        "tools": [
            "Airgeddon", "Fluxion", "Wifite2", "EAPHammer", "FakeAPBuilder"
        ]
    },
    "forensics": {
        "name": "Forensics & Reverse Engineering",
        "description": "Memory dump triage, Android APK decompiler, binary analysis, and exploit suggestion",
        "tools": [
            "Volatility3", "Apktool", "JADX", "Linux-Exploit-Suggester", "PEASS-ng"
        ]
    },
    "essential": {
        "name": "Essential Starter Kit",
        "description": "Compact, fast curated suite with the most impactful tools across all domains",
        "tools": [
            "Sherlock", "theHarvester", "SQLMap", "Nuclei", "Subfinder", "HTTPX",
            "FFUF", "Dirsearch", "RustScan", "Bettercap", "Responder", "Impacket",
            "SecLists", "THC-Hydra", "PEASS-ng"
        ]
    }
}

def get_profile_tools(profile_id):
    """Retrieve Tool instances corresponding to a preset profile."""
    pid = profile_id.strip().lower()
    if pid not in PROFILES:
        return []
    target_names = {name.lower() for name in PROFILES[pid]["tools"]}
    return [t for t in TOOL_CATALOG if t.name.lower() in target_names]

def profile_selector(target_dir_ref):
    """Interactive role-based preset profile selector."""
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.YELLOW}=== ROLE-BASED INSTALLATION PROFILES & PRESETS ==={Color.RESET}\n")
    print(f" Select a tailored security profile optimized for your specific role or workflow:\n")

    p_keys = list(PROFILES.keys())
    for idx, p_key in enumerate(p_keys, 1):
        prof = PROFILES[p_key]
        tool_count = len(prof["tools"])
        print(f"  {Color.CYAN}[{idx}]{Color.RESET} {Color.BOLD}{prof['name']:<32}{Color.RESET} {Color.PURPLE}({tool_count} tools){Color.RESET}")
        print(f"      {Color.DIM}{prof['description']}{Color.RESET}\n")

    print(f"  {Color.RED}[0]{Color.RESET} Return to main menu\n")
    choice = input(f" {Color.BOLD}Select a profile [1-{len(p_keys)}] or 0: {Color.RESET}").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(p_keys):
        selected_key = p_keys[int(choice) - 1]
        prof = PROFILES[selected_key]
        matched_tools = get_profile_tools(selected_key)
        print(f"\n {Color.GREEN}Selected Profile:{Color.RESET} {Color.BOLD}{prof['name']}{Color.RESET} ({len(matched_tools)} tools)")
        print(f" Included: {Color.DIM}{', '.join([t.name for t in matched_tools])}{Color.RESET}\n")
        confirm = input(f" {Color.YELLOW}Proceed with installation to {target_dir_ref[0]}? [Y/n]: {Color.RESET}").strip().lower()
        if confirm in ("", "y", "yes"):
            return matched_tools
    return None

# ==============================================================================
#  CLONING & INSTALLATION ENGINE (WITH ISOLATED VIRTUAL ENVIRONMENTS)
# ==============================================================================

def check_pip_break_system_packages():
    """Detect if pip supports and requires --break-system-packages (PEP 668)."""
    try:
        res = subprocess.run([sys.executable, "-m", "pip", "install", "--help"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "--break-system-packages" in res.stdout
    except Exception:
        return False

PIP_HAS_BREAK_FLAG = check_pip_break_system_packages()

def generate_tool_launcher(tool, dest_path, venv_py):
    """
    Generate executable launcher wrappers (run.sh on POSIX, run.bat on Windows)
    pointing directly to the isolated virtual environment interpreter.
    """
    try:
        # Determine entry file if available
        entry = ""
        if tool.executables:
            entry = tool.executables[0]
        else:
            candidates = [
                f"{tool.folder}.py", "main.py", "run.py", "app.py", "cli.py",
                f"{tool.folder.lower()}.py"
            ]
            for c in candidates:
                if os.path.exists(os.path.join(dest_path, c)):
                    entry = c
                    break

        # Generate run.sh for Linux/macOS
        if os.name != "nt":
            sh_path = os.path.join(dest_path, "run.sh")
            sh_content = f"""#!/usr/bin/env bash
# Auto-generated isolated launcher for {tool.name} (setup_hack_env)
DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
if [ -f "$DIR/.venv/bin/python" ]; then
    PY="$DIR/.venv/bin/python"
elif [ -f "$DIR/.venv/bin/python3" ]; then
    PY="$DIR/.venv/bin/python3"
else
    PY="python3"
fi
ENTRY="{entry}"
if [ -n "$ENTRY" ] && [ -f "$DIR/$ENTRY" ]; then
    exec "$PY" "$DIR/$ENTRY" "$@"
else
    exec "$PY" "$@"
fi
"""
            with open(sh_path, "w", encoding="utf-8") as f:
                f.write(sh_content)
            os.chmod(sh_path, 0o755)

        # Generate run.bat for Windows
        bat_path = os.path.join(dest_path, "run.bat")
        bat_content = f"""@echo off
rem Auto-generated isolated launcher for {tool.name} (setup_hack_env)
set SCRIPT_DIR=%~dp0
set VENV_PY=%SCRIPT_DIR%.venv\\Scripts\\python.exe
if not exist "%VENV_PY%" set VENV_PY=python
set ENTRY={entry}
if defined ENTRY (
    if exist "%SCRIPT_DIR%%ENTRY%" (
        "%VENV_PY%" "%SCRIPT_DIR%%ENTRY%" %*
        exit /b %ERRORLEVEL%
    )
)
"%VENV_PY%" %*
"""
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)
    except Exception:
        pass

def install_or_update_tool(tool, target_dir, log_fn=None, use_venv=True):
    """
    Robust clone and update handler.
    Supports Windows, macOS, and all Linux distributions.
    Executes commands with exact working directory (cwd).
    Features isolated virtual environments (.venv) per Python tool.
    """
    dest_path = os.path.normpath(os.path.join(target_dir, tool.folder))
    start_time = time.time()
    status_msg = ""
    success = False

    def log(msg):
        if log_fn:
            log_fn(msg)
        else:
            print(msg)

    try:
        # Step 1: Clone or Pull Repository
        if os.path.exists(dest_path):
            # Check if valid git repository
            git_check = subprocess.run(
                ["git", "-C", dest_path, "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if git_check.returncode == 0:
                log(f"  {Color.STEP} Existing repository detected. Pulling latest updates...")
                pull_res = subprocess.run(
                    ["git", "-C", dest_path, "pull", "--ff-only"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if pull_res.returncode == 0:
                    status_text = pull_res.stdout.strip()
                    if "Already up to date" in status_text:
                        status_msg = "Up-to-date"
                    else:
                        status_msg = "Updated to latest"
                else:
                    # Retry simple pull
                    fallback_pull = subprocess.run(
                        ["git", "-C", dest_path, "pull"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    status_msg = "Updated (fallback)" if fallback_pull.returncode == 0 else "Pull Warning"
            else:
                log(f"  {Color.WARN} Directory exists but is not a git repository. Skipping clone.")
                status_msg = "Existed (non-git)"
        else:
            log(f"  {Color.STEP} Cloning from official upstream ({tool.repo})...")
            # Attempt fast shallow clone first
            clone_res = subprocess.run(
                ["git", "clone", "--depth", "1", tool.repo, dest_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if clone_res.returncode != 0:
                log(f"  {Color.WARN} Shallow clone failed, retrying with full git clone...")
                clone_res = subprocess.run(
                    ["git", "clone", tool.repo, dest_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
            if clone_res.returncode != 0:
                err = clone_res.stderr.strip().splitlines()[-1] if clone_res.stderr.strip() else "Git clone failed"
                return False, f"Clone error: {err}", time.time() - start_time
            status_msg = "Cloned"

        # Step 2: Handle Dependencies & Isolated Virtual Environment
        if tool.install_type in ("pip", "pip_setup") and os.path.exists(dest_path):
            venv_pip = None
            venv_py = None
            if use_venv:
                venv_dir = os.path.join(dest_path, ".venv")
                if not os.path.exists(venv_dir):
                    log(f"  {Color.STEP} Creating isolated Python virtual environment (.venv)...")
                    try:
                        venv_res = subprocess.run(
                            [sys.executable, "-m", "venv", venv_dir],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                        )
                        if venv_res.returncode != 0:
                            venv.create(venv_dir, with_pip=True)
                    except Exception as ve:
                        log(f"  {Color.WARN} Venv notice: {ve}")

                # Detect venv pip & python binaries
                if os.name == "nt":
                    candidate_pip = os.path.join(venv_dir, "Scripts", "pip.exe")
                    candidate_py = os.path.join(venv_dir, "Scripts", "python.exe")
                else:
                    candidate_pip = os.path.join(venv_dir, "bin", "pip")
                    candidate_py = os.path.join(venv_dir, "bin", "python")

                if os.path.exists(candidate_pip):
                    venv_pip = candidate_pip
                    venv_py = candidate_py
                else:
                    # Alternative Scripts directory
                    candidate_pip_alt = os.path.join(venv_dir, "Scripts", "pip")
                    if os.path.exists(candidate_pip_alt):
                        venv_pip = candidate_pip_alt
                        venv_py = os.path.join(venv_dir, "Scripts", "python")

            if venv_pip:
                base_pip_cmd = [venv_pip, "install"]
                log(f"  {Color.SUCCESS} Isolated environment active (.venv)")
            else:
                base_pip_cmd = [sys.executable, "-m", "pip", "install"]
                if PIP_HAS_BREAK_FLAG:
                    base_pip_cmd.append("--break-system-packages")

            req_file = os.path.join(dest_path, "requirements.txt")
            if os.path.exists(req_file):
                log(f"  {Color.STEP} Installing Python dependencies from requirements.txt...")
                subprocess.run(base_pip_cmd + ["-r", "requirements.txt", "--quiet"],
                               cwd=dest_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if tool.install_type == "pip_setup":
                setup_file = os.path.join(dest_path, "setup.py")
                pyproj_file = os.path.join(dest_path, "pyproject.toml")
                if os.path.exists(setup_file) or os.path.exists(pyproj_file):
                    log(f"  {Color.STEP} Installing package via pip install . ...")
                    subprocess.run(base_pip_cmd + [".", "--quiet"],
                                   cwd=dest_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Generate launcher wrapper script
            if venv_py and os.path.exists(dest_path):
                generate_tool_launcher(tool, dest_path, venv_py)

        elif tool.install_type == "make" and os.path.exists(dest_path):
            if os.path.exists(os.path.join(dest_path, "Makefile")):
                if shutil.which("make"):
                    log(f"  {Color.STEP} Compiling via make...")
                    subprocess.run(["make", "-j4"], cwd=dest_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    log(f"  {Color.WARN} 'make' not detected on system. Skipping compile step.")

        # Step 3: Set executable permissions (POSIX only)
        if tool.executables and os.name != "nt":
            for exe_rel in tool.executables:
                exe_full = os.path.join(dest_path, exe_rel)
                if os.path.exists(exe_full):
                    try:
                        os.chmod(exe_full, 0o755)
                    except Exception:
                        pass

        # Step 4: Run any extra build commands
        if tool.extra_cmds:
            for cmd in tool.extra_cmds:
                subprocess.run(cmd, shell=True, cwd=dest_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        success = True
        elapsed = time.time() - start_time
        return True, status_msg, elapsed

    except Exception as e:
        elapsed = time.time() - start_time
        return False, str(e), elapsed

# ==============================================================================
#  UPDATE ALL INSTALLED TOOLS ENGINE
# ==============================================================================

def update_all_installed_tools(target_dir, interactive=True):
    """
    Iterate through all installed tools in the destination directory
    and update them to the latest commit using git pull.
    """
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== SMART TOOL UPDATER ==={Color.RESET}")
    print(f" Scanning directory: {Color.GREEN}{target_dir}{Color.RESET}\n")

    if not os.path.exists(target_dir):
        print(f" {Color.WARN} Directory {target_dir} does not exist yet. Please install tools first.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    subdirs = [os.path.join(target_dir, d) for d in os.listdir(target_dir)
               if os.path.isdir(os.path.join(target_dir, d))]
    
    git_repos = []
    for d in subdirs:
        if os.path.exists(os.path.join(d, ".git")):
            git_repos.append(d)

    if not git_repos:
        print(f" {Color.WARN} No Git repositories found in {target_dir}.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    print(f" Found {Color.BOLD}{len(git_repos)}{Color.RESET} installed tool repositories.\n")
    print(f" {Color.DARK}┌" + "─" * 24 + "┬" + "─" * 16 + "┬" + "─" * 30 + f"┐{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET} {Color.BOLD}{'Tool Name':<22}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Branch':<14}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Update Status':<28}{Color.RESET} {Color.DARK}│{Color.RESET}")
    print(f" {Color.DARK}├" + "─" * 24 + "┼" + "─" * 16 + "┼" + "─" * 30 + f"┤{Color.RESET}")

    updated_count = 0
    up_to_date_count = 0
    error_count = 0

    for repo_path in sorted(git_repos):
        repo_name = os.path.basename(repo_path)
        # Get active branch
        b_res = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        branch = b_res.stdout.strip() if b_res.returncode == 0 else "main"

        # Run git pull
        pull_res = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        out_text = pull_res.stdout.strip()

        if pull_res.returncode == 0:
            if "Already up to date" in out_text:
                status_badge = f"{Color.GREEN}Up to date{Color.RESET}"
                up_to_date_count += 1
            else:
                status_badge = f"{Color.CYAN}{Color.BOLD}Updated (latest commits){Color.RESET}"
                updated_count += 1
                # Check requirements update
                req_file = os.path.join(repo_path, "requirements.txt")
                if os.path.exists(req_file):
                    venv_pip = os.path.join(repo_path, ".venv", "Scripts" if os.name == "nt" else "bin", "pip.exe" if os.name == "nt" else "pip")
                    if os.path.exists(venv_pip):
                        pip_cmd = [venv_pip, "install", "-r", "requirements.txt", "--quiet"]
                    else:
                        pip_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]
                        if PIP_HAS_BREAK_FLAG:
                            pip_cmd.append("--break-system-packages")
                    subprocess.run(pip_cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            err_line = pull_res.stderr.strip().splitlines()[-1] if pull_res.stderr.strip() else "Pull conflict/error"
            status_badge = f"{Color.RED}Error: {err_line[:20]}{Color.RESET}"
            error_count += 1

        print(f" {Color.DARK}│{Color.RESET} {repo_name[:22]:<22} {Color.DARK}│{Color.RESET} {branch[:14]:<14} {Color.DARK}│{Color.RESET} {status_badge:<37} {Color.DARK}│{Color.RESET}")

    print(f" {Color.DARK}└" + "─" * 24 + "┴" + "─" * 16 + "┴" + "─" * 30 + f"┘{Color.RESET}\n")
    print(f" {Color.BOLD}Update Summary:{Color.RESET}")
    print(f"   {Color.SUCCESS} Already Latest : {up_to_date_count}")
    print(f"   {Color.STEP} Freshly Updated: {updated_count}")
    if error_count > 0:
        print(f"   {Color.ERROR} Errors/Diverged: {error_count}")
    print()
    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")

# ==============================================================================
#  CROSS-PLATFORM SYSTEM PREREQUISITES & PACKAGE MANAGER SETUP
# ==============================================================================

def install_system_prerequisites(interactive=True):
    """
    Install base security tools, Python headers, wordlists, and network utilities
    across all supported platforms:
      - Linux: Debian, Kali, Parrot, Ubuntu (apt), Arch, Manjaro (pacman),
               Fedora, RHEL (dnf/yum), openSUSE (zypper), Alpine (apk)
      - macOS: Homebrew (brew)
      - Windows: Winget / Chocolatey
    """
    clear_screen()
    display_banner()
    info = PLATFORM_INFO
    print(f" {Color.BOLD}{Color.YELLOW}=== SYSTEM PREREQUISITES & ENVIRONMENT CONFIGURATION ==={Color.RESET}\n")
    print(f" Detected Platform : {Color.CYAN}{info['os_name']} ({info['os_type']}){Color.RESET}")
    print(f" Package Manager   : {Color.PURPLE}{info['pkg_manager_name']}{Color.RESET}")
    print(f" Privilege Status  : {'Elevated (Admin/Root)' if info['is_admin'] else 'Standard User'}\n")

    pm = info["pkg_manager"]
    is_root = info["is_admin"]
    sudo_prefix = [] if is_root or os.name == "nt" else ["sudo"]

    if not pm:
        print(f" {Color.WARN} No supported package manager detected automatically.")
        if info["os_type"] == "Windows":
            print(f" {Color.INFO} On Windows, you can install tools using Winget or Chocolatey:")
            print("   winget install --id Git.Git -e --source winget")
            print("   winget install --id Python.Python.3.12 -e --source winget")
            print("   winget install --id Insecure.Nmap -e --source winget")
        elif info["os_type"] == "macOS":
            print(f" {Color.INFO} On macOS, install Homebrew first by running:")
            print('   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        else:
            print(f" {Color.INFO} Please install git, python3-pip, and base build tools using your Linux distribution package manager.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    if interactive and sys.stdin.isatty():
        confirm = input(f" {Color.BOLD}Proceed with installing prerequisites for {info['os_name']} via {pm}? [y/N]: {Color.RESET}").strip().lower()
        if confirm != "y":
            print(f" {Color.INFO} Operation cancelled.")
            time.sleep(1)
            return

    # Dispatch to OS-specific package manager
    if pm == "apt":
        print(f"\n {Color.STEP} Updating APT package indices...")
        subprocess.run(sudo_prefix + ["apt", "update", "-y"])
        core_packages = [
            "build-essential", "libssl-dev", "libffi-dev", "curl", "wget", "git",
            "python3-pip", "python3-venv", "python3-dev", "net-tools", "dnsutils",
            "tor", "proxychains4", "neofetch", "htop", "gzip", "p7zip-full",
            "zipalign", "apksigner", "nmap", "tcpdump", "traceroute", "whois"
        ]
        print(f" {Color.STEP} Installing core Linux packages...")
        subprocess.run(sudo_prefix + ["apt", "install", "-y"] + core_packages)

        # Wordlists setup: extract rockyou.txt if still gzipped
        rockyou_gz = "/usr/share/wordlists/rockyou.txt.gz"
        rockyou_txt = "/usr/share/wordlists/rockyou.txt"
        if os.path.exists(rockyou_gz) and not os.path.exists(rockyou_txt):
            print(f" {Color.STEP} Extracting rockyou.txt wordlist...")
            subprocess.run(sudo_prefix + ["gzip", "-d", "-k", rockyou_gz])
            print(f" {Color.SUCCESS} rockyou.txt extracted to /usr/share/wordlists/rockyou.txt")

    elif pm == "pacman":
        print(f"\n {Color.STEP} Installing core packages via Pacman (Arch Linux / Manjaro)...")
        arch_packages = [
            "base-devel", "openssl", "libffi", "curl", "wget", "git",
            "python", "python-pip", "python-virtualenv", "net-tools", "dnsutils",
            "tor", "proxychains-ng", "neofetch", "htop", "p7zip",
            "nmap", "tcpdump", "traceroute", "whois"
        ]
        subprocess.run(sudo_prefix + ["pacman", "-Sy", "--noconfirm", "--needed"] + arch_packages)

    elif pm in ("dnf", "yum"):
        print(f"\n {Color.STEP} Installing core packages via {pm} (Fedora / RHEL / CentOS)...")
        rpm_packages = [
            "make", "automake", "gcc", "gcc-c++", "openssl-devel", "libffi-devel",
            "curl", "wget", "git", "python3", "python3-pip", "python3-devel",
            "net-tools", "bind-utils", "tor", "proxychains-ng", "neofetch", "htop",
            "p7zip", "p7zip-plugins", "nmap", "tcpdump", "traceroute", "whois"
        ]
        subprocess.run(sudo_prefix + [pm, "install", "-y"] + rpm_packages)

    elif pm == "zypper":
        print(f"\n {Color.STEP} Installing core packages via Zypper (openSUSE)...")
        subprocess.run(sudo_prefix + ["zypper", "install", "-y", "-t", "pattern", "devel_basis"])
        suse_packages = [
            "libopenssl-devel", "libffi-devel", "curl", "wget", "git",
            "python3", "python3-pip", "python3-devel", "net-tools-deprecated",
            "bind-utils", "tor", "proxychains", "neofetch", "htop", "p7zip",
            "nmap", "whois"
        ]
        subprocess.run(sudo_prefix + ["zypper", "install", "-y"] + suse_packages)

    elif pm == "apk":
        print(f"\n {Color.STEP} Installing core packages via APK (Alpine Linux)...")
        apk_packages = [
            "build-base", "openssl-dev", "libffi-dev", "curl", "wget", "git",
            "python3", "py3-pip", "python3-dev", "net-tools", "bind-tools",
            "tor", "proxychains-ng", "neofetch", "htop", "7zip",
            "nmap", "whois"
        ]
        subprocess.run(sudo_prefix + ["apk", "add"] + apk_packages)

    elif pm == "brew":
        print(f"\n {Color.STEP} Installing packages via Homebrew (macOS)...")
        brew_packages = [
            "git", "curl", "wget", "python", "nmap", "htop",
            "tor", "proxychains-ng", "p7zip", "whois"
        ]
        subprocess.run(["brew", "install"] + brew_packages)

    elif pm == "winget":
        print(f"\n {Color.STEP} Installing Windows packages via Winget...")
        subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget", "--accept-source-agreements", "--accept-package-agreements"])
        subprocess.run(["winget", "install", "--id", "Python.Python.3.12", "-e", "--source", "winget", "--accept-source-agreements", "--accept-package-agreements"])
        subprocess.run(["winget", "install", "--id", "Insecure.Nmap", "-e", "--source", "winget", "--accept-source-agreements", "--accept-package-agreements"])

    elif pm == "choco":
        print(f"\n {Color.STEP} Installing Windows packages via Chocolatey...")
        subprocess.run(["choco", "install", "-y", "git", "python", "nmap"])

    print(f"\n {Color.SUCCESS} Prerequisites installation completed!")
    if interactive and sys.stdin.isatty():
        input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")

# ==============================================================================
#  CROSS-PLATFORM KEYBOARD INPUT HANDLER
# ==============================================================================

def read_key():
    """
    Read a single keystroke from standard input across Windows, macOS, and Linux.
    Supports arrow keys, space, enter, backspace, tab, page up, page down, and shortcuts.
    """
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            ch2 = msvcrt.getwch()
            key_map = {
                "H": "UP",
                "P": "DOWN",
                "K": "LEFT",
                "M": "RIGHT",
                "I": "PAGE_UP",
                "Q": "PAGE_DOWN",
                "G": "HOME",
                "O": "END",
            }
            return key_map.get(ch2, "ESC")
        elif ch in ("\r", "\n"):
            return "ENTER"
        elif ch == " ":
            return "SPACE"
        elif ch in ("\x08", "\x7f"):
            return "BACKSPACE"
        elif ch == "\t":
            return "TAB"
        elif ch == "\x03":  # Ctrl+C
            return "CTRL_C"
        elif ch == "\x1b":  # Escape
            return "ESC"
        return ch
    else:
        import termios
        import tty
        import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":  # Escape sequence
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        r2, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if r2:
                            ch3 = sys.stdin.read(1)
                            if ch3 == "A":
                                return "UP"
                            elif ch3 == "B":
                                return "DOWN"
                            elif ch3 == "C":
                                return "RIGHT"
                            elif ch3 == "D":
                                return "LEFT"
                            elif ch3 == "H":
                                return "HOME"
                            elif ch3 == "F":
                                return "END"
                            elif ch3 in ("5", "6"):
                                sys.stdin.read(1)  # Consume '~'
                                return "PAGE_UP" if ch3 == "5" else "PAGE_DOWN"
                            return "ESC"
                        return "ESC"
                    elif ch2 == "O":  # Application cursor key mode
                        ch3 = sys.stdin.read(1)
                        if ch3 == "A":
                            return "UP"
                        if ch3 == "B":
                            return "DOWN"
                        if ch3 == "H":
                            return "HOME"
                        if ch3 == "F":
                            return "END"
                        return "ESC"
                return "ESC"
            elif ch in ("\r", "\n"):
                return "ENTER"
            elif ch == " ":
                return "SPACE"
            elif ch in ("\x7f", "\x08"):
                return "BACKSPACE"
            elif ch == "\t":
                return "TAB"
            elif ch == "\x03":  # Ctrl+C
                return "CTRL_C"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# ==============================================================================
#  INTERACTIVE CHECKBOX TOOL SELECTOR (WITH LIVE SEARCH FILTER)
# ==============================================================================

def interactive_checkbox_selector(tools, target_dir_ref):
    """
    Full-featured interactive terminal checkbox multi-selector with live search filtering.
    Features:
      - Live search filter: Press [/] or type query to dynamically filter tools
      - Spacebar toggle for checkboxes: [✓] / [ ]
      - Up / Down (or k / j) to navigate smoothly
      - 'a' key: Select All / Deselect All visible matches
      - 'c' key: Toggle entire category of focused item
      - 'd' key: Edit destination directory
      - Enter: Confirm selection and proceed with installation
      - 'q' or Esc: Cancel and return
      - Dynamic viewport scrolling fitting any terminal window height.
    """
    selected = {t.name: True for t in tools}
    cursor = 0
    total_tools = len(tools)
    target_dir = target_dir_ref[0]
    search_query = ""
    search_mode = False

    # Hide terminal cursor for flicker-free rendering
    if Color.ENABLED:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    try:
        while True:
            # Filter tools according to search query
            if search_query:
                q = search_query.lower()
                filtered_tools = [
                    t for t in tools
                    if q in t.name.lower() or q in t.category.lower() or q in t.description.lower()
                ]
            else:
                filtered_tools = tools

            num_filtered = len(filtered_tools)
            if num_filtered == 0:
                cursor = 0
            else:
                cursor = max(0, min(cursor, num_filtered - 1))

            term_w = get_terminal_width()
            term_h = get_terminal_height()

            # Reserve lines for header, search bar, controls, footer
            header_lines = 11
            footer_lines = 4
            page_size = max(5, term_h - header_lines - footer_lines)

            # Viewport scrolling window
            scroll_offset = max(0, min(cursor - page_size // 2, max(0, num_filtered - page_size)))
            visible_tools = filtered_tools[scroll_offset : scroll_offset + page_size]

            selected_count = sum(1 for v in selected.values() if v)
            visible_selected = sum(1 for t in filtered_tools if selected.get(t.name, False))

            # Build frame in buffer
            buf = []
            buf.append("\033[H\033[J")  # Clear screen and move cursor home
            buf.append(f"{Color.CYAN}{Color.BOLD}╔" + "═" * (term_w - 4) + f"╗{Color.RESET}\n")
            buf.append(f"{Color.CYAN}{Color.BOLD}║  ☑  INTERACTIVE TOOL CHECKBOX SELECTOR (WITH LIVE SEARCH)" + " " * max(0, term_w - 61) + f"║{Color.RESET}\n")
            buf.append(f"{Color.CYAN}{Color.BOLD}╚" + "═" * (term_w - 4) + f"╝{Color.RESET}\n")

            # Search bar & Status line
            if search_mode:
                search_display = f"{Color.BG_BLUE}{Color.WHITE}{Color.BOLD} SEARCH MODE {Color.RESET} {Color.YELLOW}[{search_query}█]{Color.RESET}  {Color.DIM}(Type query, [Enter/Esc] to exit search mode){Color.RESET}"
            else:
                if search_query:
                    search_display = f"{Color.PURPLE}{Color.BOLD}Active Filter:{Color.RESET} '{Color.YELLOW}{search_query}{Color.RESET}' ({num_filtered}/{total_tools} matched)  {Color.DIM}(Press [/] to edit filter, [x] to clear){Color.RESET}"
                else:
                    search_display = f"{Color.DIM}Search Filter: [Press '/' to search and filter tools dynamically]{Color.RESET}"

            buf.append(f" {search_display}\n")
            buf.append(
                f" {Color.BOLD}Selected:{Color.RESET} {Color.GREEN}{selected_count}/{total_tools}{Color.RESET} total "
                f"({Color.CYAN}{visible_selected}/{num_filtered}{Color.RESET} visible)  "
                f"{Color.DIM}│{Color.RESET}  {Color.BOLD}Target Dir:{Color.RESET} {Color.CYAN}{target_dir}{Color.RESET}\n"
            )
            buf.append(
                f" {Color.DIM}Controls: [/] Search │ [↑/↓] Navigate │ [Space] Check │ [a] All In Filter │ [c] Cat │ [Enter] Install │ [q] Back{Color.RESET}\n"
            )
            buf.append(f" {Color.DARK}" + "─" * (term_w - 2) + f"{Color.RESET}\n")

            # Render visible tools
            if not visible_tools:
                buf.append(f"\n   {Color.WARN} No tools matched filter '{search_query}'. Press [/] to change or [x] to clear.\n\n")
            else:
                for i, tool in enumerate(visible_tools):
                    global_idx = scroll_offset + i
                    is_cursor = (global_idx == cursor)
                    is_checked = selected.get(tool.name, False)

                    checkbox = f"{Color.GREEN}{Color.BOLD}[✓]{Color.RESET}" if is_checked else f"{Color.GRAY}[ ]{Color.RESET}"
                    pointer = f"{Color.CYAN}{Color.BOLD}➜{Color.RESET} " if is_cursor else "  "

                    name_styled = f"{Color.BOLD}{Color.WHITE}{tool.name:<20}{Color.RESET}" if is_cursor else f"{tool.name:<20}"
                    cat_badge = f"{Color.PURPLE}[{tool.category[:15]}]{Color.RESET}"
                    desc = tool.description[:max(10, term_w - 55)]

                    line = f"{pointer}{checkbox} {name_styled} {cat_badge:<25} {Color.DIM}{desc}{Color.RESET}"
                    buf.append(line + "\n")

            # Fill blank lines if terminal is large
            for _ in range(page_size - len(visible_tools)):
                buf.append("\n")

            buf.append(f" {Color.DARK}" + "─" * (term_w - 2) + f"{Color.RESET}\n")
            pos_info = f"Item {cursor + 1}/{num_filtered} (Showing {scroll_offset + 1}-{min(scroll_offset + page_size, num_filtered)} of {num_filtered})" if num_filtered > 0 else "0 tools matched"
            buf.append(f" {Color.DIM}{pos_info:<40}{Color.RESET}\n")

            sys.stdout.write("".join(buf))
            sys.stdout.flush()

            # Read user keystroke
            key = read_key()

            if search_mode:
                if key in ("ESC", "ENTER"):
                    search_mode = False
                elif key == "BACKSPACE":
                    search_query = search_query[:-1]
                elif key == "TAB":
                    search_mode = False
                elif len(key) == 1 and key.isprintable():
                    search_query += key
                continue

            # Standard Navigation Mode
            if key == "/":
                search_mode = True
            elif key in ("x", "X") and search_query:
                search_query = ""
            elif key in ("UP", "k", "K"):
                cursor = max(0, cursor - 1)
            elif key in ("DOWN", "j", "J"):
                cursor = min(max(0, num_filtered - 1), cursor + 1)
            elif key == "PAGE_UP":
                cursor = max(0, cursor - page_size)
            elif key == "PAGE_DOWN":
                cursor = min(max(0, num_filtered - 1), cursor + page_size)
            elif key == "HOME":
                cursor = 0
            elif key == "END":
                cursor = max(0, num_filtered - 1)
            elif key == "SPACE":
                if num_filtered > 0:
                    tool_name = filtered_tools[cursor].name
                    selected[tool_name] = not selected.get(tool_name, False)
            elif key in ("a", "A"):
                # Toggle all visible filtered tools
                if num_filtered > 0:
                    all_vis_selected = all(selected.get(t.name, False) for t in filtered_tools)
                    for t in filtered_tools:
                        selected[t.name] = not all_vis_selected
            elif key in ("c", "C"):
                # Toggle entire category of the active item
                if num_filtered > 0:
                    current_cat = filtered_tools[cursor].category
                    cat_tools = [t for t in filtered_tools if t.category == current_cat]
                    cat_all_on = all(selected.get(t.name, False) for t in cat_tools)
                    for t in cat_tools:
                        selected[t.name] = not cat_all_on
            elif key in ("d", "D"):
                # Change destination directory
                sys.stdout.write("\033[?25h")
                sys.stdout.flush()
                print(f"\n {Color.BOLD}Current target directory:{Color.RESET} {Color.CYAN}{target_dir}{Color.RESET}")
                new_dir = input(f" {Color.YELLOW}Enter new directory path (or press Enter to keep current): {Color.RESET}").strip()
                if new_dir:
                    target_dir = os.path.abspath(os.path.expanduser(new_dir))
                    target_dir_ref[0] = target_dir
                if Color.ENABLED:
                    sys.stdout.write("\033[?25l")
                    sys.stdout.flush()
            elif key == "ENTER":
                chosen = [t for t in tools if selected.get(t.name, False)]
                return chosen
            elif key in ("q", "Q", "ESC", "CTRL_C"):
                return None

    finally:
        if Color.ENABLED:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

# ==============================================================================
#  FALLBACK NUMBERED SELECTOR (FOR PIPES / NON-TTY ENVIRONMENTS)
# ==============================================================================

def fallback_numbered_selector(tools):
    """Fallback tool selector when running in non-TTY or automated shells."""
    print(f"\n {Color.BOLD}Available Tools Catalog:{Color.RESET}\n")
    for idx, t in enumerate(tools, 1):
        print(f"  [{idx:2d}] {t.name:<22} [{t.category:<20}] - {t.description}")
    print()
    print(f" {Color.INFO} Enter tool numbers (e.g. 1, 3, 5-10), 'all', or 'q' to cancel.")
    choice = input(f" {Color.YELLOW}Your selection: {Color.RESET}").strip().lower()

    if choice in ("q", "cancel", "exit"):
        return []
    if choice == "all":
        return tools

    selected = set()
    parts = choice.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                for i in range(int(start), int(end) + 1):
                    if 1 <= i <= len(tools):
                        selected.add(i - 1)
            except ValueError:
                pass
        else:
            try:
                i = int(part)
                if 1 <= i <= len(tools):
                    selected.add(i - 1)
            except ValueError:
                pass

    return [tools[i] for i in sorted(selected)]

# ==============================================================================
#  CATEGORY SELECTOR SCREEN
# ==============================================================================

def category_selector(target_dir_ref):
    """Allow user to select and install tools by high-level category."""
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== CATEGORY TOOL SELECTOR ==={Color.RESET}\n")

    cat_map = {}
    for t in TOOL_CATALOG:
        cat_map.setdefault(t.category, []).append(t)

    print(f" {Color.BOLD}Available Categories:{Color.RESET}\n")
    cat_list = list(cat_map.keys())
    for idx, cat_name in enumerate(cat_list, 1):
        tool_count = len(cat_map[cat_name])
        sample_tools = ", ".join(t.name for t in cat_map[cat_name][:3]) + "..."
        print(f"  {Color.CYAN}[{idx}]{Color.RESET} {Color.BOLD}{cat_name:<26}{Color.RESET} ({tool_count} tools) {Color.DIM}- e.g. {sample_tools}{Color.RESET}")

    print(f"\n  {Color.YELLOW}[A]{Color.RESET} Select ALL Categories (All {len(TOOL_CATALOG)} tools)")
    print(f"  {Color.RED}[0]{Color.RESET} Return to Main Menu\n")

    choice = input(f" {Color.BOLD}Enter category number(s) separated by comma (e.g. 1, 2, 4): {Color.RESET}").strip()
    if choice == "0" or not choice:
        return []
    if choice.upper() == "A":
        return TOOL_CATALOG

    selected_tools = []
    for part in choice.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(cat_list):
                selected_tools.extend(cat_map[cat_list[idx]])

    return selected_tools

# ==============================================================================
#  BATCH INSTALLATION RUNNER WITH REAL-TIME FEEDBACK
# ==============================================================================

def run_installation_batch(selected_tools, target_dir, interactive=True, use_venv=True):
    """
    Execute installation across selected tools.
    Displays live step-by-step progress, timestamps, and summary cards.
    """
    if not selected_tools:
        print(f"\n {Color.WARN} No tools selected for installation.")
        time.sleep(1.5)
        return

    clear_screen()
    display_banner()

    os.makedirs(target_dir, exist_ok=True)
    total = len(selected_tools)
    total_start = time.time()

    print(f" {Color.BOLD}{Color.GREEN}=== EXECUTING INSTALLATION BATCH ==={Color.RESET}")
    print(f" Destination Directory : {Color.CYAN}{target_dir}{Color.RESET}")
    print(f" Total Tools Selected  : {Color.BOLD}{total}{Color.RESET}")
    print(f" Environment Mode      : {'Isolated Python .venv per tool' if use_venv else 'System Global Interpreter'}\n")

    successful = []
    failed = []

    for idx, tool in enumerate(selected_tools, 1):
        print(f" {Color.DARK}┌─[{Color.RESET} {Color.BOLD}TOOL {idx}/{total}{Color.RESET}: {Color.CYAN}{Color.BOLD}{tool.name}{Color.RESET} {Color.PURPLE}[{tool.category}]{Color.RESET} {Color.DARK}]" + "─" * 25 + f"┐{Color.RESET}")
        print(f" {Color.DARK}│{Color.RESET}  {Color.DIM}{tool.description}{Color.RESET}")
        print(f" {Color.DARK}│{Color.RESET}  Source: {Color.BLUE}{tool.repo}{Color.RESET}")

        ok, msg, elapsed = install_or_update_tool(tool, target_dir, use_venv=use_venv)

        if ok:
            print(f" {Color.DARK}└─▶{Color.RESET} {Color.SUCCESS} {Color.BOLD}{tool.name}{Color.RESET} finished: {Color.GREEN}{msg}{Color.RESET} {Color.DIM}({elapsed:.2f}s){Color.RESET}\n")
            successful.append((tool.name, msg, elapsed))
        else:
            print(f" {Color.DARK}└─▶{Color.RESET} {Color.ERROR} {Color.BOLD}{tool.name}{Color.RESET} failed: {Color.RED}{msg}{Color.RESET} {Color.DIM}({elapsed:.2f}s){Color.RESET}\n")
            failed.append((tool.name, msg, elapsed))

    # Print Installation Summary Card
    total_elapsed = time.time() - total_start
    print(f" {Color.PURPLE}╔" + "═" * 68 + f"╗{Color.RESET}")
    print(f" {Color.PURPLE}║  {Color.YELLOW}{Color.BOLD}★ INSTALLATION SUMMARY ★{Color.RESET}" + " " * 44 + f"{Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}╠" + "═" * 68 + f"╣{Color.RESET}")
    print(f" {Color.PURPLE}║{Color.RESET}  {Color.BOLD}Total Processed{Color.RESET}    : {total:<46} {Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}║{Color.RESET}  {Color.SUCCESS} Successful     : {Color.GREEN}{len(successful):<46}{Color.RESET} {Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}║{Color.RESET}  {Color.ERROR} Failed/Warnings: {Color.RED}{len(failed):<46}{Color.RESET} {Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}║{Color.RESET}  {Color.BOLD}Time Elapsed{Color.RESET}       : {f'{total_elapsed:.1f} seconds':<46} {Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}║{Color.RESET}  {Color.BOLD}Destination Path{Color.RESET}   : {Color.CYAN}{target_dir[:46]:<46}{Color.RESET} {Color.PURPLE}║{Color.RESET}")
    print(f" {Color.PURPLE}╚" + "═" * 68 + f"╝{Color.RESET}\n")

    if failed:
        print(f" {Color.WARN} Failed tools detail:")
        for name, err, _ in failed:
            print(f"   - {Color.BOLD}{name}{Color.RESET}: {Color.RED}{err}{Color.RESET}")
        print()

    # Time-based personalized greeting
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if 4 <= hour < 12 else ("Good afternoon" if 12 <= hour < 17 else ("Good evening" if 17 <= hour < 21 else "Good night"))
    print(f" {Color.GREEN}{Color.BOLD}{greeting}, {socket.gethostname()}! Happy Hacking!{Color.RESET}\n")
    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")

# ==============================================================================
#  CATALOG VIEW & SOURCE AUDIT
# ==============================================================================

def display_tool_catalog(interactive=True):
    """Display all curated tools and their authentic upstream source URLs."""
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== ETHICAL HACKING TOOLS CATALOG ({len(TOOL_CATALOG)} TOOLS) ==={Color.RESET}\n")

    current_cat = None
    for t in TOOL_CATALOG:
        if t.category != current_cat:
            current_cat = t.category
            print(f"\n {Color.YELLOW}{Color.BOLD}── {current_cat.upper()} ──{Color.RESET}")
        print(f"  {Color.GREEN}•{Color.RESET} {Color.BOLD}{t.name:<22}{Color.RESET} {Color.BLUE}{t.repo:<54}{Color.RESET}")
        print(f"    {Color.DIM}{t.description}{Color.RESET}")

    print()
    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")

# ==============================================================================
#  SYSTEM DOCTOR & PRE-FLIGHT DIAGNOSTICS (FEATURE 5)
# ==============================================================================

def check_socket_latency(host, port=443, timeout=3.0):
    """Measure raw TCP socket connection latency in milliseconds."""
    start = time.time()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return round((time.time() - start) * 1000, 1)
    except Exception:
        return None

def check_command_output(cmd, timeout=4):
    """Run command safely and extract first line of output."""
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip().splitlines()[0]
        elif res.stderr.strip():
            return res.stderr.strip().splitlines()[0]
        return None
    except Exception:
        return None

def run_doctor_diagnostics(interactive=True):
    """
    Comprehensive environment doctor:
      - Validates operating system, kernel, and virtualization (Docker/WSL/Baremetal)
      - Inspects compilers and runtimes: Python, Git, Go, Rust/Cargo, Node, NPM, Ruby, Gem, Make, GCC/Clang, Docker
      - Inspects security packages: Nmap, Tor, Proxychains, TCPDump
      - Verifies disk storage capacity and target volume health
      - Tests live network latency to GitHub, PyPI, and DNS
      - Computes an overall environment health score with copy-paste remediation commands.
    """
    clear_screen()
    display_banner()
    info = PLATFORM_INFO

    print(f" {Color.BOLD}{Color.YELLOW}=== PRE-FLIGHT ENVIRONMENT DOCTOR & SYSTEM DIAGNOSTICS ==={Color.RESET}\n")

    # 1. System & Virtualization
    virt_type = "Bare Metal / Standard Host"
    if os.path.exists("/.dockerenv") or os.path.exists("/run/systemd/container"):
        virt_type = "Docker Container"
    elif "microsoft" in platform.uname().release.lower():
        virt_type = "WSL (Windows Subsystem for Linux)"

    print(f" {Color.BOLD}1. OPERATING SYSTEM & ARCHITECTURE{Color.RESET}")
    print(f"   • OS Platform      : {Color.CYAN}{info['os_name']} ({info['os_type']}){Color.RESET}")
    print(f"   • Kernel & Arch    : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"   • Environment Type : {Color.PURPLE}{virt_type}{Color.RESET}")
    print(f"   • Privilege Level  : {'Elevated (Admin/Root)' if info['is_admin'] else 'Standard User'}")
    print(f"   • Python Runtime   : {sys.version.split()[0]} ({sys.executable})\n")

    # 2. Runtimes & Compilers
    print(f" {Color.BOLD}2. RUNTIMES, COMPILERS & BUILD TOOLS AUDIT{Color.RESET}")
    print(f"   {Color.DARK}┌" + "─" * 18 + "┬" + "─" * 10 + "┬" + "─" * 28 + "┬" + "─" * 22 + f"┐{Color.RESET}")
    print(f"   {Color.DARK}│{Color.RESET} {Color.BOLD}{'Runtime/Tool':<16}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Status':<8}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Version / Path':<26}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Required For':<20}{Color.RESET} {Color.DARK}│{Color.RESET}")
    print(f"   {Color.DARK}├" + "─" * 18 + "┼" + "─" * 10 + "┼" + "─" * 28 + "┼" + "─" * 22 + f"┤{Color.RESET}")

    runtimes = [
        ("Git", ["git", "--version"], True, "Cloning & auto-pulls"),
        ("Python 3", [sys.executable, "--version"], True, "Python security tools"),
        ("Pip", [sys.executable, "-m", "pip", "--version"], True, "Python package manager"),
        ("Go (Golang)", ["go", "version"], False, "HTTPX, Nuclei, Katana"),
        ("Cargo (Rust)", ["cargo", "--version"], False, "RustScan, Sniffnet"),
        ("Node.js", ["node", "--version"], False, "JS recon & API security"),
        ("NPM", ["npm", "--version"], False, "Node package manager"),
        ("Ruby", ["ruby", "--version"], False, "CeWL, WPScan"),
        ("Gem", ["gem", "--version"], False, "Ruby package manager"),
        ("Make", ["make", "--version"], False, "C/C++ compilation"),
        ("GCC / Clang", ["gcc", "--version"] if shutil.which("gcc") else ["clang", "--version"], False, "Native code build"),
        ("Docker", ["docker", "--version"], False, "Sandbox container"),
    ]

    missing_critical = []
    missing_optional = []
    total_score = 100

    for name, cmd, is_crit, purpose in runtimes:
        bin_name = cmd[0] if cmd else name
        found = shutil.which(bin_name) or (name == "Python 3") or (name == "Pip")
        if found:
            out = check_command_output(cmd)
            v_str = out[:26] if out else "Installed"
            v_str = v_str.replace("version ", "v").replace("go version ", "")
            status = f"{Color.GREEN}PASS{Color.RESET}"
            print(f"   {Color.DARK}│{Color.RESET} {name:<16} {Color.DARK}│{Color.RESET} {status:<17} {Color.DARK}│{Color.RESET} {v_str:<26} {Color.DARK}│{Color.RESET} {Color.DIM}{purpose[:20]:<20}{Color.RESET} {Color.DARK}│{Color.RESET}")
        else:
            status = f"{Color.RED}FAIL{Color.RESET}" if is_crit else f"{Color.YELLOW}WARN{Color.RESET}"
            print(f"   {Color.DARK}│{Color.RESET} {name:<16} {Color.DARK}│{Color.RESET} {status:<17} {Color.DARK}│{Color.RESET} {'Not Found':<26} {Color.DARK}│{Color.RESET} {Color.DIM}{purpose[:20]:<20}{Color.RESET} {Color.DARK}│{Color.RESET}")
            if is_crit:
                missing_critical.append(name)
                total_score -= 20
            else:
                missing_optional.append(name)
                total_score -= 5

    print(f"   {Color.DARK}└" + "─" * 18 + "┴" + "─" * 10 + "┴" + "─" * 28 + "┴" + "─" * 22 + f"┘{Color.RESET}\n")

    # 3. Pre-Installed Security Binaries
    print(f" {Color.BOLD}3. PRE-INSTALLED SYSTEM UTILITIES{Color.RESET}")
    sec_utils = ["nmap", "tor", "proxychains4" if shutil.which("proxychains4") else "proxychains", "tcpdump", "wireshark"]
    for util in sec_utils:
        path = shutil.which(util)
        if path:
            print(f"   • {util:<14}: {Color.GREEN}Available{Color.RESET} ({Color.DIM}{path}{Color.RESET})")
        else:
            print(f"   • {util:<14}: {Color.DIM}Not installed in PATH{Color.RESET}")
    print()

    # 4. Storage & Volume Health
    print(f" {Color.BOLD}4. STORAGE & VOLUME HEALTH{Color.RESET}")
    try:
        cwd_usage = shutil.disk_usage(os.getcwd())
        free_gb = cwd_usage.free / (1024**3)
        total_gb = cwd_usage.total / (1024**3)
        pct_used = (cwd_usage.used / cwd_usage.total) * 100
        disk_status = f"{Color.GREEN}Optimal{Color.RESET}" if free_gb >= 15 else (f"{Color.YELLOW}Adequate{Color.RESET}" if free_gb >= 5 else f"{Color.RED}Critical Low{Color.RESET}")
        print(f"   • Working Volume   : {disk_status} - {free_gb:.1f} GB free of {total_gb:.1f} GB ({pct_used:.1f}% used)")
        if free_gb < 5:
            total_score -= 15
            print(f"     {Color.WARN} Less than 5 GB remaining. Cloning large repos may exhaust space.")
    except Exception as e:
        print(f"   • Storage check notice: {e}")
    print()

    # 5. Network Connectivity & Latency
    print(f" {Color.BOLD}5. NETWORK CONNECTIVITY & LATENCY{Color.RESET}")
    github_lat = check_socket_latency("github.com", 443)
    pypi_lat = check_socket_latency("pypi.org", 443)
    dns_start = time.time()
    try:
        socket.gethostbyname("github.com")
        dns_lat = round((time.time() - dns_start) * 1000, 1)
        dns_str = f"{Color.GREEN}{dns_lat} ms{Color.RESET}"
    except Exception:
        dns_str = f"{Color.RED}Failed{Color.RESET}"
        total_score -= 15

    gh_str = f"{Color.GREEN}{github_lat} ms{Color.RESET}" if github_lat is not None else f"{Color.RED}Unreachable{Color.RESET}"
    pypi_str = f"{Color.GREEN}{pypi_lat} ms{Color.RESET}" if pypi_lat is not None else f"{Color.RED}Unreachable{Color.RESET}"

    if github_lat is None:
        total_score -= 25

    print(f"   • DNS Resolution (github.com) : {dns_str}")
    print(f"   • GitHub.com TLS Latency      : {gh_str}")
    print(f"   • PyPI.org TLS Latency        : {pypi_str}\n")

    # 6. Overall Health Score & Recommendations
    total_score = max(0, min(100, total_score))
    score_color = Color.GREEN if total_score >= 80 else (Color.YELLOW if total_score >= 50 else Color.RED)

    print(f" {Color.BOLD}6. DIAGNOSTIC SUMMARY & HEALTH SCORE{Color.RESET}")
    print(f"   Health Score : {score_color}{Color.BOLD}{total_score}/100{Color.RESET}")

    if total_score >= 90:
        print(f"   Status       : {Color.GREEN}System is in prime condition for ethical hacking & pentesting.{Color.RESET}")
    elif total_score >= 70:
        print(f"   Status       : {Color.YELLOW}System is ready, but optional runtimes (Go, Rust, or Ruby) will unlock more tools.{Color.RESET}")
    else:
        print(f"   Status       : {Color.RED}Action required: Missing essential build runtimes or network access.{Color.RESET}")

    if missing_critical or missing_optional:
        print(f"\n {Color.BOLD}Recommended Installation Commands for {info['os_name']}:{Color.RESET}")
        pm = info["pkg_manager"]
        if pm == "apt":
            pkgs = []
            if "Go (Golang)" in missing_optional: pkgs.append("golang-go")
            if "Cargo (Rust)" in missing_optional: pkgs.append("cargo")
            if "Node.js" in missing_optional or "NPM" in missing_optional: pkgs.extend(["nodejs", "npm"])
            if "Ruby" in missing_optional: pkgs.append("ruby-full")
            if "Make" in missing_optional or "GCC / Clang" in missing_optional: pkgs.append("build-essential")
            if "Docker" in missing_optional: pkgs.append("docker.io")
            if pkgs:
                print(f"   {Color.CYAN}sudo apt update && sudo apt install -y {' '.join(pkgs)}{Color.RESET}")
        elif pm == "brew":
            pkgs = []
            if "Go (Golang)" in missing_optional: pkgs.append("go")
            if "Cargo (Rust)" in missing_optional: pkgs.append("rust")
            if "Node.js" in missing_optional or "NPM" in missing_optional: pkgs.append("node")
            if "Ruby" in missing_optional: pkgs.append("ruby")
            if "Docker" in missing_optional: pkgs.append("docker")
            if pkgs:
                print(f"   {Color.CYAN}brew install {' '.join(pkgs)}{Color.RESET}")
        elif pm == "pacman":
            pkgs = []
            if "Go (Golang)" in missing_optional: pkgs.append("go")
            if "Cargo (Rust)" in missing_optional: pkgs.append("rust")
            if "Node.js" in missing_optional: pkgs.append("nodejs")
            if "Ruby" in missing_optional: pkgs.append("ruby")
            if "Make" in missing_optional: pkgs.append("base-devel")
            if pkgs:
                print(f"   {Color.CYAN}sudo pacman -S --needed {' '.join(pkgs)}{Color.RESET}")
        elif pm in ("dnf", "yum"):
            pkgs = []
            if "Go (Golang)" in missing_optional: pkgs.append("golang")
            if "Cargo (Rust)" in missing_optional: pkgs.append("cargo")
            if "Node.js" in missing_optional: pkgs.append("nodejs")
            if "Ruby" in missing_optional: pkgs.append("ruby")
            if pkgs:
                print(f"   {Color.CYAN}sudo {pm} install -y {' '.join(pkgs)}{Color.RESET}")
        elif pm == "winget":
            print(f"   {Color.CYAN}winget install GoLang.Go{Color.RESET}")
            print(f"   {Color.CYAN}winget install Rustlang.Rustup{Color.RESET}")
            print(f"   {Color.CYAN}winget install OpenJS.NodeJS.LTS{Color.RESET}")

    print()
    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")

# ==============================================================================
#  DISK SPACE & STORAGE MANAGER (FEATURE 9)
# ==============================================================================

def format_bytes(byte_count):
    """Format bytes into human-readable B, KB, MB, GB, TB string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(byte_count)
    unit_idx = 0
    while size >= 1024.0 and unit_idx < len(units) - 1:
        size /= 1024.0
        unit_idx += 1
    return f"{size:.2f} {units[unit_idx]}"

def get_directory_size_and_count(dir_path):
    """Calculate recursive total byte size and file count."""
    total_size = 0
    file_count = 0
    try:
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
                        file_count += 1
                except (OSError, FileNotFoundError):
                    pass
    except Exception:
        pass
    return total_size, file_count

def run_storage_manager(target_dir, interactive=True):
    """
    Inspect disk footprint of all installed tools in target directory,
    displaying size ranking table and volume usage metrics.
    """
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== DISK SPACE & STORAGE MANAGER ==={Color.RESET}")
    print(f" Target Directory: {Color.GREEN}{target_dir}{Color.RESET}\n")

    if not os.path.exists(target_dir):
        print(f" {Color.WARN} Target directory does not exist yet. No tools installed.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    subdirs = [os.path.join(target_dir, d) for d in os.listdir(target_dir)
               if os.path.isdir(os.path.join(target_dir, d))]

    if not subdirs:
        print(f" {Color.WARN} No tool folders found in {target_dir}.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    print(f" {Color.STEP} Analyzing disk space for {len(subdirs)} tool folders (this may take a few seconds)...")
    tool_sizes = []
    total_tools_bytes = 0

    for d in subdirs:
        folder_name = os.path.basename(d)
        size, fcount = get_directory_size_and_count(d)
        total_tools_bytes += size

        # Check git commit count if repo
        commits = "-"
        if os.path.exists(os.path.join(d, ".git")):
            c_res = subprocess.run(["git", "-C", d, "rev-list", "--count", "HEAD"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if c_res.returncode == 0:
                commits = c_res.stdout.strip()

        has_venv = os.path.exists(os.path.join(d, ".venv"))
        tool_sizes.append((folder_name, size, fcount, commits, has_venv))

    # Sort descending by size
    tool_sizes.sort(key=lambda x: x[1], reverse=True)

    print(f"\n {Color.DARK}┌" + "─" * 4 + "┬" + "─" * 26 + "┬" + "─" * 14 + "┬" + "─" * 10 + "┬" + "─" * 10 + "┬" + "─" * 8 + f"┐{Color.RESET}")
    print(f" {Color.DARK}│{Color.RESET} {Color.BOLD}{'#':<2}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Tool Folder':<24}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Disk Size':<12}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Files':<8}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'Commits':<8}{Color.RESET} {Color.DARK}│{Color.RESET} {Color.BOLD}{'.venv':<6}{Color.RESET} {Color.DARK}│{Color.RESET}")
    print(f" {Color.DARK}├" + "─" * 4 + "┼" + "─" * 26 + "┼" + "─" * 14 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 8 + f"┤{Color.RESET}")

    for idx, (name, size, fcount, commits, has_venv) in enumerate(tool_sizes[:25], 1):
        v_str = f"{Color.GREEN}yes{Color.RESET}" if has_venv else f"{Color.DIM}no{Color.RESET}"
        print(f" {Color.DARK}│{Color.RESET} {idx:<2} {Color.DARK}│{Color.RESET} {name[:24]:<24} {Color.DARK}│{Color.RESET} {Color.BOLD}{format_bytes(size):<12}{Color.RESET} {Color.DARK}│{Color.RESET} {fcount:<8} {Color.DARK}│{Color.RESET} {commits:<8} {Color.DARK}│{Color.RESET} {v_str:<15} {Color.DARK}│{Color.RESET}")

    print(f" {Color.DARK}└" + "─" * 4 + "┴" + "─" * 26 + "┴" + "─" * 14 + "┴" + "─" * 10 + "┴" + "─" * 10 + "┴" + "─" * 8 + f"┘{Color.RESET}")

    if len(tool_sizes) > 25:
        print(f" {Color.DIM}... and {len(tool_sizes) - 25} more tools not shown.{Color.RESET}")

    print(f"\n {Color.BOLD}Storage Summary:{Color.RESET}")
    print(f"   • Total Space Consumed : {Color.GREEN}{Color.BOLD}{format_bytes(total_tools_bytes)}{Color.RESET} in {len(tool_sizes)} tool directories")

    try:
        usage = shutil.disk_usage(target_dir)
        print(f"   • Free Volume Space    : {Color.CYAN}{format_bytes(usage.free)}{Color.RESET} of {format_bytes(usage.total)}")
    except Exception:
        pass

    if interactive and sys.stdin.isatty():
        print(f"\n {Color.BOLD}Options:{Color.RESET} [c] Run disk cache cleaner │ [Enter] Return to main menu")
        act = input(f" {Color.YELLOW}Select an action: {Color.RESET}").strip().lower()
        if act == "c":
            clean_storage_cache(target_dir, interactive=True)

def clean_storage_cache(target_dir, interactive=True):
    """
    Purge Python bytecode (__pycache__, *.pyc), pytest caches, temporary build files,
    and run 'git gc' to optimize loose object storage.
    """
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.YELLOW}=== DISK SPACE CLEANER & CACHE PURGER ==={Color.RESET}")
    print(f" Target Directory: {Color.CYAN}{target_dir}{Color.RESET}\n")

    if not os.path.exists(target_dir):
        print(f" {Color.WARN} Target directory does not exist.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return...{Color.RESET}")
        return

    print(f" {Color.STEP} Scanning for removable caches, bytecode, and temp files...")

    pycache_dirs = []
    cache_dirs = []
    pyc_files = []
    bytes_found = 0

    cache_dir_names = {".pytest_cache", ".mypy_cache", ".tox", ".coverage", ".cache"}

    for root, dirs, files in os.walk(target_dir):
        for d in list(dirs):
            if d == "__pycache__":
                full_p = os.path.join(root, d)
                pycache_dirs.append(full_p)
                sz, _ = get_directory_size_and_count(full_p)
                bytes_found += sz
            elif d in cache_dir_names:
                full_p = os.path.join(root, d)
                cache_dirs.append(full_p)
                sz, _ = get_directory_size_and_count(full_p)
                bytes_found += sz

        for f in files:
            if f.endswith((".pyc", ".pyo", ".pyd")):
                full_f = os.path.join(root, f)
                pyc_files.append(full_f)
                try:
                    bytes_found += os.path.getsize(full_f)
                except Exception:
                    pass

    git_repos = [os.path.join(target_dir, d) for d in os.listdir(target_dir)
                 if os.path.isdir(os.path.join(target_dir, d)) and os.path.exists(os.path.join(target_dir, d, ".git"))]

    print(f"   • Python Bytecode Directories (__pycache__) : {len(pycache_dirs)}")
    print(f"   • Test & Tool Cache Directories            : {len(cache_dirs)}")
    print(f"   • Orphan Bytecode Files (*.pyc)             : {len(pyc_files)}")
    print(f"   • Git Repositories Eligible for 'git gc'    : {len(git_repos)}")
    print(f"   • Estimated Space Reclaimable               : {Color.GREEN}{Color.BOLD}{format_bytes(bytes_found)}{Color.RESET}\n")

    if not pycache_dirs and not cache_dirs and not pyc_files and not git_repos:
        print(f" {Color.SUCCESS} Everything is clean! No temporary caches found.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return...{Color.RESET}")
        return

    if interactive and sys.stdin.isatty():
        conf = input(f" {Color.BOLD}Proceed with purging caches and running git gc optimization? [Y/n]: {Color.RESET}").strip().lower()
        if conf not in ("", "y", "yes"):
            print(f" {Color.INFO} Cleaning cancelled.")
            time.sleep(1)
            return

    freed_bytes = 0
    for p in pycache_dirs:
        try:
            sz, _ = get_directory_size_and_count(p)
            shutil.rmtree(p, ignore_errors=True)
            freed_bytes += sz
        except Exception:
            pass

    for c in cache_dirs:
        try:
            sz, _ = get_directory_size_and_count(c)
            shutil.rmtree(c, ignore_errors=True)
            freed_bytes += sz
        except Exception:
            pass

    for f in pyc_files:
        try:
            sz = os.path.getsize(f)
            os.remove(f)
            freed_bytes += sz
        except Exception:
            pass

    print(f" {Color.STEP} Running git garbage collection and repository repacking...")
    for repo in git_repos:
        subprocess.run(["git", "-C", repo, "gc", "--auto", "--quiet"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f"\n {Color.SUCCESS} Disk cleanup complete! Reclaimed {Color.GREEN}{Color.BOLD}{format_bytes(freed_bytes)}{Color.RESET} of disk space.\n")
    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return...{Color.RESET}")

# ==============================================================================
#  CONFIGURATION EXPORT & IMPORT (FEATURE 7)
# ==============================================================================

def export_configuration(target_dir, filepath=None, interactive=True):
    """
    Export current installation state, tools list, git commits, and environment
    metadata into a reproducible JSON manifest.
    """
    if not filepath:
        default_file = os.path.join(target_dir, "setup-hack-manifest.json")
        if interactive and sys.stdin.isatty():
            clear_screen()
            display_banner()
            print(f" {Color.BOLD}{Color.CYAN}=== EXPORT TOOL ENVIRONMENT MANIFEST ==={Color.RESET}\n")
            print(f" Target Directory : {Color.GREEN}{target_dir}{Color.RESET}")
            ans = input(f" {Color.YELLOW}Enter export file path (or press Enter for '{default_file}'): {Color.RESET}").strip()
            filepath = os.path.abspath(os.path.expanduser(ans)) if ans else default_file
        else:
            filepath = default_file

    if not os.path.exists(target_dir):
        print(f" {Color.ERROR} Target directory {target_dir} does not exist.")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return...{Color.RESET}")
        return False

    subdirs = [os.path.join(target_dir, d) for d in os.listdir(target_dir)
               if os.path.isdir(os.path.join(target_dir, d))]

    installed_tools = []
    catalog_by_folder = {t.folder.lower(): t for t in TOOL_CATALOG}

    for d in sorted(subdirs):
        folder_name = os.path.basename(d)
        if folder_name.startswith(".") or folder_name in ("__pycache__", "assets"):
            continue
        is_git = os.path.exists(os.path.join(d, ".git"))
        commit = ""
        branch = ""
        repo_url = ""

        if is_git:
            c_res = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if c_res.returncode == 0:
                commit = c_res.stdout.strip()

            b_res = subprocess.run(["git", "-C", d, "rev-parse", "--abbrev-ref", "HEAD"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if b_res.returncode == 0:
                branch = b_res.stdout.strip()

            r_res = subprocess.run(["git", "-C", d, "config", "--get", "remote.origin.url"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if r_res.returncode == 0:
                repo_url = r_res.stdout.strip()

        cat_tool = catalog_by_folder.get(folder_name.lower())
        tool_name = cat_tool.name if cat_tool else folder_name
        category = cat_tool.category if cat_tool else "Custom"
        if not repo_url and cat_tool:
            repo_url = cat_tool.repo

        has_venv = os.path.exists(os.path.join(d, ".venv"))

        installed_tools.append({
            "name": tool_name,
            "folder": folder_name,
            "repo": repo_url,
            "branch": branch,
            "commit": commit,
            "category": category,
            "has_venv": has_venv
        })

    manifest = {
        "manifest_version": "1.0.0",
        "app": "setup_hack_env",
        "version": "4.0.0",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "platform": {
            "os_name": PLATFORM_INFO["os_name"],
            "os_type": PLATFORM_INFO["os_type"],
            "architecture": platform.machine()
        },
        "target_dir": target_dir,
        "tool_count": len(installed_tools),
        "tools": installed_tools
    }

    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"\n {Color.SUCCESS} Environment manifest successfully exported!")
        print(f"   • Path         : {Color.CYAN}{filepath}{Color.RESET}")
        print(f"   • Tools Count  : {Color.BOLD}{len(installed_tools)}{Color.RESET} tools recorded")
        print(f"   • File Size    : {format_bytes(os.path.getsize(filepath))}\n")
    except Exception as e:
        print(f"\n {Color.ERROR} Failed to write manifest: {e}\n")
        return False

    if interactive and sys.stdin.isatty():
        input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
    return True

def import_configuration(filepath, target_dir=None, interactive=True, use_venv=True):
    """
    Import and restore an environment from a setup-hack JSON manifest.
    """
    if not os.path.exists(filepath):
        print(f" {Color.ERROR} Manifest file not found: {filepath}")
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return...{Color.RESET}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f" {Color.ERROR} Failed to parse manifest JSON: {e}")
        return False

    tools_data = data.get("tools", [])
    if not tools_data:
        print(f" {Color.WARN} No tools found in manifest.")
        return False

    dest = target_dir or data.get("target_dir") or str(Path.home() / "Tools")

    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== IMPORT TOOL ENVIRONMENT MANIFEST ==={Color.RESET}\n")
    print(f" Manifest File    : {Color.GREEN}{filepath}{Color.RESET}")
    print(f" Created On       : {data.get('timestamp', 'Unknown')}")
    print(f" Source OS        : {data.get('platform', {}).get('os_name', 'Unknown')}")
    print(f" Target Directory : {Color.CYAN}{dest}{Color.RESET}")
    print(f" Total Tools      : {Color.BOLD}{len(tools_data)}{Color.RESET}\n")

    catalog_by_name = {t.name.lower(): t for t in TOOL_CATALOG}
    tools_to_install = []

    for t_item in tools_data:
        name = t_item.get("name", "")
        repo = t_item.get("repo", "")
        folder = t_item.get("folder", "")
        category = t_item.get("category", "Imported")
        has_venv = t_item.get("has_venv", False)

        cat_tool = catalog_by_name.get(name.lower())
        if cat_tool:
            tools_to_install.append(cat_tool)
        elif repo and folder:
            custom_t = Tool(
                name=name or folder,
                repo=repo,
                folder=folder,
                category=category,
                description=f"Manifest imported repository: {name}",
                install_type="pip" if has_venv else "none"
            )
            tools_to_install.append(custom_t)

    if interactive and sys.stdin.isatty():
        confirm = input(f" {Color.BOLD}Proceed with installing {len(tools_to_install)} tools to {dest}? [Y/n]: {Color.RESET}").strip().lower()
        if confirm not in ("", "y", "yes"):
            print(f" {Color.INFO} Import aborted by user.")
            time.sleep(1)
            return False

    run_installation_batch(tools_to_install, dest, interactive=interactive, use_venv=use_venv)
    return True

# ==============================================================================
#  DOCKER SANDBOX & CONTAINERIZED ENVIRONMENT (FEATURE 6)
# ==============================================================================

DOCKERFILE_CONTENT = """# SETUP_HACK_ENV: Containerized Ethical Hacking & Penetration Testing Suite
FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color
ENV LANG=C.UTF-8

WORKDIR /opt/setup_hack_env

# Install core Linux build tools, python, git, go, curl, and network essentials
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    git \\
    curl \\
    wget \\
    python3 \\
    python3-pip \\
    python3-venv \\
    python3-dev \\
    golang-go \\
    libssl-dev \\
    libffi-dev \\
    p7zip-full \\
    net-tools \\
    dnsutils \\
    whois \\
    nmap \\
    tcpdump \\
    ca-certificates \\
    && rm -rf /var/lib/apt/lists/*

# Copy repository contents into container
COPY . /opt/setup_hack_env/

# Create persistent tools mount directory
RUN mkdir -p /tools && chmod 777 /tools

ENV TOOLS_DIR=/tools
WORKDIR /opt/setup_hack_env

ENTRYPOINT ["python3", "setup-hack.py", "--dir", "/tools"]
"""

DOCKER_COMPOSE_CONTENT = """version: "3.8"

services:
  setup-hack:
    build:
      context: .
      dockerfile: Dockerfile
    image: setup-hack-env:latest
    container_name: setup_hack_container
    stdin_open: true
    tty: true
    network_mode: host
    volumes:
      - ./tools:/tools
    environment:
      - TERM=xterm-256color
    restart: unless-stopped
"""

def create_docker_artifacts(repo_dir=None):
    """Generate root Dockerfile and docker-compose.yml files."""
    base_dir = repo_dir or os.path.dirname(os.path.abspath(__file__))
    df_path = os.path.join(base_dir, "Dockerfile")
    dc_path = os.path.join(base_dir, "docker-compose.yml")

    created = []
    if not os.path.exists(df_path):
        with open(df_path, "w", encoding="utf-8") as f:
            f.write(DOCKERFILE_CONTENT)
        created.append("Dockerfile")

    if not os.path.exists(dc_path):
        with open(dc_path, "w", encoding="utf-8") as f:
            f.write(DOCKER_COMPOSE_CONTENT)
        created.append("docker-compose.yml")

    return created

def setup_docker_environment(interactive=True):
    """
    Manage containerized Docker sandbox environment:
      - Verify Docker installation
      - Generate Dockerfile & docker-compose.yml
      - Build image and launch interactive container shell
    """
    clear_screen()
    display_banner()
    print(f" {Color.BOLD}{Color.CYAN}=== DOCKER CONTAINER SANDBOX ENVIRONMENT ==={Color.RESET}\n")

    docker_bin = shutil.which("docker")
    if not docker_bin:
        print(f" {Color.ERROR} Docker is not installed or not available in system PATH!")
        print(f" {Color.INFO} Install Docker to run tools in an isolated sandbox without host modification:")
        info = PLATFORM_INFO
        if info["os_type"] == "macOS":
            print(f"   Download Docker Desktop for Mac: https://www.docker.com/products/docker-desktop/")
            print(f"   Or run: brew install --cask docker")
        elif info["os_type"] == "Windows":
            print(f"   Download Docker Desktop for Windows: https://www.docker.com/products/docker-desktop/")
            print(f"   Or run: winget install Docker.DockerDesktop")
        else:
            print(f"   Debian/Ubuntu/Kali: sudo apt install -y docker.io docker-compose")
            print(f"   Arch Linux        : sudo pacman -S docker docker-compose")
            print(f"   Fedora            : sudo dnf install -y docker docker-compose")
        print()
        if interactive and sys.stdin.isatty():
            input(f" {Color.DIM}Press Enter to return to main menu...{Color.RESET}")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_path = os.path.join(base_dir, "Dockerfile")
    dc_path = os.path.join(base_dir, "docker-compose.yml")

    if not os.path.exists(df_path) or not os.path.exists(dc_path):
        created = create_docker_artifacts(base_dir)
        if created:
            print(f" {Color.SUCCESS} Generated container artifacts: {', '.join(created)}")

    print(f" Docker Status : {Color.GREEN}Available ({docker_bin}){Color.RESET}")
    print(f" Dockerfile    : {Color.DIM}{df_path}{Color.RESET}")
    print(f" Compose File  : {Color.DIM}{dc_path}{Color.RESET}\n")

    print(f" {Color.BOLD}Select a Docker action:{Color.RESET}\n")
    print(f"  {Color.CYAN}[1]{Color.RESET} {Color.BOLD}🔨 Build Docker Sandbox Image{Color.RESET}     {Color.DIM}- Build setup-hack-env:latest{Color.RESET}")
    print(f"  {Color.CYAN}[2]{Color.RESET} {Color.BOLD}🚀 Launch Interactive Container{Color.RESET}       {Color.DIM}- Run setup-hack inside Docker (tools mounted to ./tools){Color.RESET}")
    print(f"  {Color.CYAN}[3]{Color.RESET} {Color.BOLD}🎯 Run Role Profile in Docker{Color.RESET}         {Color.DIM}- e.g. install bug-bounty in container{Color.RESET}")
    print(f"  {Color.CYAN}[4]{Color.RESET} {Color.BOLD}🔄 Refresh Dockerfile & Compose{Color.RESET}       {Color.DIM}- Overwrite with latest Kali template{Color.RESET}")
    print(f"  {Color.RED}[0]{Color.RESET} Return to main menu\n")

    choice = input(f" {Color.BOLD}Select option [0-4]: {Color.RESET}").strip()

    if choice == "1":
        print(f"\n {Color.STEP} Building Docker image 'setup-hack-env:latest'...")
        subprocess.run(["docker", "build", "-t", "setup-hack-env:latest", base_dir])
        if interactive and sys.stdin.isatty():
            input(f"\n {Color.DIM}Press Enter to return...{Color.RESET}")
    elif choice == "2":
        print(f"\n {Color.STEP} Starting containerized session...")
        tools_mount = os.path.abspath(os.path.join(base_dir, "tools"))
        os.makedirs(tools_mount, exist_ok=True)
        if shutil.which("docker-compose"):
            subprocess.run(["docker-compose", "run", "--rm", "setup-hack"], cwd=base_dir)
        else:
            subprocess.run(["docker", "run", "-it", "--rm", "-v", f"{tools_mount}:/tools", "setup-hack-env:latest"])
    elif choice == "3":
        prof_name = input(f"\n {Color.YELLOW}Enter profile name (e.g. bug-bounty, osint, red-team): {Color.RESET}").strip()
        if prof_name:
            tools_mount = os.path.abspath(os.path.join(base_dir, "tools"))
            os.makedirs(tools_mount, exist_ok=True)
            subprocess.run(["docker", "run", "-it", "--rm", "-v", f"{tools_mount}:/tools", "setup-hack-env:latest", "--profile", prof_name])
    elif choice == "4":
        with open(df_path, "w", encoding="utf-8") as f:
            f.write(DOCKERFILE_CONTENT)
        with open(dc_path, "w", encoding="utf-8") as f:
            f.write(DOCKER_COMPOSE_CONTENT)
        print(f"\n {Color.SUCCESS} Refreshed Dockerfile and docker-compose.yml successfully!")
        time.sleep(1.5)

# ==============================================================================
#  GIT CHECK UTILITY
# ==============================================================================

def check_git_installed():
    """Verify that Git is installed and available in system PATH."""
    if not shutil.which("git"):
        info = PLATFORM_INFO
        print(f"\n {Color.ERROR} Git is not installed or not found in system PATH!")
        if info["os_type"] == "Windows":
            print(f" {Color.INFO} Download Git for Windows from: https://git-scm.com/download/win")
            print(f" {Color.INFO} Or run: winget install --id Git.Git -e --source winget")
        elif info["os_type"] == "macOS":
            print(f" {Color.INFO} Install Git via Homebrew: brew install git")
            print(f" {Color.INFO} Or via Xcode Command Line Tools: xcode-select --install")
        else:
            print(f" {Color.INFO} Install Git via your Linux distribution's package manager:")
            print(f"   Debian/Kali/Ubuntu : sudo apt install -y git")
            print(f"   Arch/Manjaro       : sudo pacman -S git")
            print(f"   Fedora/RHEL        : sudo dnf install -y git")
            print(f"   Alpine Linux       : sudo apk add git")
        print()
        return False
    return True

# ==============================================================================
#  MAIN INTERACTIVE MENU
# ==============================================================================

def main_menu(default_target_dir):
    """Central interactive menu loop."""
    target_dir_ref = [default_target_dir]

    while True:
        clear_screen()
        display_banner()
        display_status_header(target_dir_ref[0])

        print(f" {Color.BOLD}PRIMARY ACTIONS:{Color.RESET}\n")
        print(f"  {Color.CYAN}[1]{Color.RESET}  {Color.BOLD}⚡ Quick Install All Tools{Color.RESET}        {Color.DIM}- Install complete 65+ curated tool suite{Color.RESET}")
        print(f"  {Color.CYAN}[2]{Color.RESET}  {Color.BOLD}🗂  Category Selector{Color.RESET}              {Color.DIM}- Choose tools by security domain{Color.RESET}")
        print(f"  {Color.CYAN}[3]{Color.RESET}  {Color.BOLD}🎯 Role Presets & Profiles{Color.RESET}        {Color.DIM}- Bug Bounty, OSINT, Red Team, Wireless, Forensics{Color.RESET}")
        print(f"  {Color.CYAN}[4]{Color.RESET}  {Color.BOLD}☑  Interactive Checkbox Selector{Color.RESET}  {Color.DIM}- Spacebar select with live search filter [/]{Color.RESET}")
        print(f"  {Color.CYAN}[5]{Color.RESET}  {Color.BOLD}🔄 Update All Installed Tools{Color.RESET}      {Color.DIM}- Git pull updater across existing repos{Color.RESET}")
        print(f"  {Color.CYAN}[6]{Color.RESET}  {Color.BOLD}🩺 Pre-Flight System Doctor{Color.RESET}        {Color.DIM}- Compilers, runtimes, latency, disk health{Color.RESET}")
        print(f"  {Color.CYAN}[7]{Color.RESET}  {Color.BOLD}💾 Storage Manager & Disk Cleaner{Color.RESET} {Color.DIM}- Inspect tool disk usage and purge caches{Color.RESET}")
        print(f"  {Color.CYAN}[8]{Color.RESET}  {Color.BOLD}📦 Export / Import Setup Manifest{Color.RESET} {Color.DIM}- Save or restore reproducible environments{Color.RESET}")
        print(f"  {Color.CYAN}[9]{Color.RESET}  {Color.BOLD}🐳 Docker Container Sandbox{Color.RESET}       {Color.DIM}- Isolated containerized environment{Color.RESET}")
        print(f"  {Color.CYAN}[10]{Color.RESET} {Color.BOLD}🛠  System Prerequisites & Apt{Color.RESET}    {Color.DIM}- Core Linux headers, Tor, Wordlists, build tools{Color.RESET}")
        print(f"  {Color.CYAN}[11]{Color.RESET} {Color.BOLD}📁 Change Destination Directory{Color.RESET}  {Color.DIM}- Current: {target_dir_ref[0]}{Color.RESET}")
        print(f"  {Color.CYAN}[12]{Color.RESET} {Color.BOLD}📋 View Tool Catalog & Sources{Color.RESET}   {Color.DIM}- Inspect official upstream repositories{Color.RESET}")
        print(f"  {Color.RED}[0]{Color.RESET}  {Color.BOLD}🚪 Exit{Color.RESET}\n")

        choice = input(f" {Color.BOLD}Select an option [0-12]: {Color.RESET}").strip()

        if choice == "1":
            confirm = input(f" {Color.YELLOW}Install ALL {len(TOOL_CATALOG)} tools to {target_dir_ref[0]}? [y/N]: {Color.RESET}").strip().lower()
            if confirm == "y":
                run_installation_batch(TOOL_CATALOG, target_dir_ref[0], interactive=True)
        elif choice == "2":
            selected = category_selector(target_dir_ref)
            if selected:
                run_installation_batch(selected, target_dir_ref[0], interactive=True)
        elif choice == "3":
            selected = profile_selector(target_dir_ref)
            if selected:
                run_installation_batch(selected, target_dir_ref[0], interactive=True)
        elif choice == "4":
            if sys.stdin.isatty():
                selected = interactive_checkbox_selector(TOOL_CATALOG, target_dir_ref)
            else:
                selected = fallback_numbered_selector(TOOL_CATALOG)
            if selected:
                run_installation_batch(selected, target_dir_ref[0], interactive=True)
        elif choice == "5":
            update_all_installed_tools(target_dir_ref[0], interactive=True)
        elif choice == "6":
            run_doctor_diagnostics(interactive=True)
        elif choice == "7":
            run_storage_manager(target_dir_ref[0], interactive=True)
        elif choice == "8":
            print(f"\n {Color.BOLD}Manifest Actions:{Color.RESET} [1] Export current setup │ [2] Import manifest")
            m_act = input(f" {Color.YELLOW}Choose [1/2]: {Color.RESET}").strip()
            if m_act == "1":
                export_configuration(target_dir_ref[0], interactive=True)
            elif m_act == "2":
                m_file = input(f" {Color.YELLOW}Enter manifest JSON file path: {Color.RESET}").strip()
                if m_file:
                    import_configuration(os.path.abspath(os.path.expanduser(m_file)), target_dir_ref[0], interactive=True)
        elif choice == "9":
            setup_docker_environment(interactive=True)
        elif choice == "10":
            install_system_prerequisites(interactive=True)
        elif choice == "11":
            print(f"\n {Color.BOLD}Current target directory:{Color.RESET} {Color.CYAN}{target_dir_ref[0]}{Color.RESET}")
            new_path = input(f" {Color.YELLOW}Enter new destination directory path: {Color.RESET}").strip()
            if new_path:
                target_dir_ref[0] = os.path.abspath(os.path.expanduser(new_path))
                print(f" {Color.SUCCESS} Destination directory set to: {target_dir_ref[0]}")
                time.sleep(1)
        elif choice == "12":
            display_tool_catalog(interactive=True)
        elif choice in ("0", "q", "exit"):
            print(f"\n {Color.GREEN}Exiting. Stay ethical and keep learning!{Color.RESET}\n")
            sys.exit(0)

# ==============================================================================
#  CLI ARGUMENT PARSING & ENTRYPOINT
# ==============================================================================

def main():
    default_dir = os.path.normpath(str(Path.home() / "Tools"))
    parser = argparse.ArgumentParser(
        description="SETUP_HACK_ENV: Advanced Ethical Hacking & Penetration Testing Suite"
    )
    parser.add_argument("-a", "--all", action="store_true", help="Install all tools without interactive prompts")
    parser.add_argument("-p", "--profile", type=str, help="Install specific role profile (e.g. bug-bounty, osint, red-team, network, wireless, forensics, essential)")
    parser.add_argument("--list-profiles", action="store_true", help="List all available preset profiles and included tools")
    parser.add_argument("-u", "--update", action="store_true", help="Update all installed tools in target directory")
    parser.add_argument("-l", "--list", action="store_true", help="List all available tools and official links")
    parser.add_argument("-d", "--dir", type=str, default=default_dir, help=f"Destination directory for cloning tools (default: {default_dir})")
    parser.add_argument("-c", "--category", type=str, help="Install specific category (comma-separated)")
    parser.add_argument("-t", "--tools", type=str, help="Install specific tool names (comma-separated, e.g. sherlock,sqlmap)")
    parser.add_argument("--doctor", action="store_true", help="Run pre-flight environment diagnostics and compiler checks")
    parser.add_argument("--storage", action="store_true", help="Inspect disk footprint and storage metrics of installed tools")
    parser.add_argument("--clean", action="store_true", help="Purge Python bytecode, test caches, and optimize git repositories")
    parser.add_argument("--export", nargs="?", const="", type=str, help="Export installed tools manifest JSON")
    parser.add_argument("--import", dest="import_file", type=str, help="Import and install tools from manifest JSON")
    parser.add_argument("--docker", action="store_true", help="Launch or manage containerized Docker sandbox")
    parser.add_argument("--venv", action="store_true", default=True, help="Use isolated virtual environments (.venv) per tool (default: True)")
    parser.add_argument("--no-venv", action="store_false", dest="venv", help="Disable isolated virtual environments, use global python")
    parser.add_argument("--deps", action="store_true", help="Install core Linux/macOS/Windows dependencies and packages")
    parser.add_argument("--no-interactive", action="store_true", help="Disable raw TTY interactive screens")

    args = parser.parse_args()
    target_dir = os.path.abspath(os.path.expanduser(args.dir))
    use_venv = args.venv

    # Fast path CLI flags
    if args.list_profiles:
        print(f"\n {Color.BOLD}{Color.YELLOW}=== AVAILABLE ROLE PROFILES ==={Color.RESET}\n")
        for p_key, prof in PROFILES.items():
            print(f"  {Color.CYAN}{p_key:<16}{Color.RESET} - {Color.BOLD}{prof['name']}{Color.RESET} ({len(prof['tools'])} tools)")
            print(f"    {Color.DIM}{prof['description']}{Color.RESET}")
            print(f"    Tools: {', '.join(prof['tools'][:8])}...")
            print()
        return

    if args.doctor:
        run_doctor_diagnostics(interactive=False)
        return

    if args.storage:
        run_storage_manager(target_dir, interactive=False)
        return

    if args.clean:
        clean_storage_cache(target_dir, interactive=False)
        return

    if args.export is not None:
        export_file = args.export if args.export else os.path.join(target_dir, "setup-hack-manifest.json")
        export_configuration(target_dir, filepath=export_file, interactive=False)
        return

    if args.import_file:
        import_configuration(os.path.abspath(os.path.expanduser(args.import_file)), target_dir, interactive=False, use_venv=use_venv)
        return

    if args.docker:
        setup_docker_environment(interactive=False)
        return

    if args.list:
        display_tool_catalog(interactive=False)
        return

    if args.deps:
        install_system_prerequisites(interactive=False)
        return

    # Check git before performing clone or update operations
    if (args.all or args.update or args.tools or args.category or args.profile) and not check_git_installed():
        sys.exit(1)

    if args.update:
        update_all_installed_tools(target_dir, interactive=False)
        return

    if args.profile:
        matched_tools = get_profile_tools(args.profile)
        if not matched_tools:
            print(f" {Color.ERROR} Unknown profile '{args.profile}'. Available profiles: {', '.join(PROFILES.keys())}")
            sys.exit(1)
        run_installation_batch(matched_tools, target_dir, interactive=False, use_venv=use_venv)
        return

    if args.tools:
        req_tools = [t.strip().lower() for t in args.tools.split(",")]
        matched_tools = [t for t in TOOL_CATALOG if t.name.lower() in req_tools or t.folder.lower() in req_tools]
        if not matched_tools:
            print(f" {Color.ERROR} No tools matched '{args.tools}'. Use --list to inspect available tools.")
            sys.exit(1)
        run_installation_batch(matched_tools, target_dir, interactive=False, use_venv=use_venv)
        return

    if args.all:
        run_installation_batch(TOOL_CATALOG, target_dir, interactive=False, use_venv=use_venv)
        return

    if args.category:
        req_cats = [c.strip().lower() for c in args.category.split(",")]
        matched_tools = [t for t in TOOL_CATALOG if t.category.lower() in req_cats or any(rc in t.category.lower() for rc in req_cats)]
        if not matched_tools:
            print(f" {Color.ERROR} No categories matched '{args.category}'. Available categories:")
            for c in CATEGORIES:
                print(f"   - {c}")
            sys.exit(1)
        run_installation_batch(matched_tools, target_dir, interactive=False, use_venv=use_venv)
        return

    # Check git before opening interactive menu
    check_git_installed()

    # Default: Launch rich interactive menu
    try:
        main_menu(target_dir)
    except KeyboardInterrupt:
        print(f"\n\n {Color.WARN} Process aborted by user. Exiting gracefully.{Color.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
