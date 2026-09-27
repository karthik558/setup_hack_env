# Setup Hack Environment (Cross-Platform: Windows, macOS, Linux)

An advanced, enterprise-grade ethical hacking and penetration testing environment automated installer. Fully cross-platform, supporting **Windows 10/11**, **macOS** (Apple Silicon & Intel), and **all Linux distributions** (Kali Linux, Parrot OS, Debian, Ubuntu, Arch Linux, Manjaro, BlackArch, Fedora, RHEL, CentOS, openSUSE, Alpine Linux, etc.).

Curated with **65+ top-tier cybersecurity tools** fetched directly from their **authentic upstream sources** (ProjectDiscovery, SQLMapProject, Sherlock-Project, Rapid7, and more).

Includes an **interactive terminal checkbox selector** (native arrow keys across Windows `msvcrt` and POSIX `termios`), a **dedicated one-click auto-updater**, custom Cyberpunk ANSI styling, and robust error-tolerant cloning.

![Banner](assets/script-linux.png)

---

## Key Highlights & Cross-Platform Architecture

- **Full Cross-Platform Support**:
  - **Linux (All Distros)**: Native support for Debian/Kali/Parrot (`apt`), Arch/Manjaro/BlackArch (`pacman`), Fedora/RHEL/CentOS (`dnf`/`yum`), openSUSE (`zypper`), and Alpine (`apk`).
  - **macOS**: Native support on Apple Silicon (M1/M2/M3/M4) & Intel with Homebrew integration.
  - **Windows**: Native support on Windows 10/11 (PowerShell / Windows Terminal / CMD) with `winget`/`choco` support and `msvcrt` raw key capture.
- **100% Authentic Upstream Sources**: No third-party forks or obsolete organizations. Every tool is cloned directly from its official creators and foundations.
- **Cleaned Catalog**: Removed broken and outdated tools (UPI-OSINT, TruecallerJS, deprecated scripts).
- **Interactive Terminal Checkbox UI**:
  - `[Up/Down]` Navigate smoothly across all tools (works on Windows, macOS, Linux)
  - `[Space]` Toggle tool selection [X] / [ ]
  - `[a]` Select All / Deselect All
  - `[c]` Toggle entire category
  - `[d]` Change destination directory on the fly
  - `[Enter]` Start installation
- **Smart Git Auto-Updater**:
  - Automatically scans your tools folder (`~/Tools` or custom directory)
  - Runs `git pull` across all installed repositories
  - Reports branch, commit status (Up to date, Updated, Diverged), and auto-updates Python `requirements.txt`
- **Fault-Tolerant Cloning Engine**:
  - No fragile `os.chdir()` cascades
  - Fast shallow clones (`--depth 1`) with full clone fallback
  - Detects existing repositories and pulls updates instead of erroring
  - Modern Python PEP 668 compliance (`--break-system-packages` auto-detection)
  - Automatic `chmod +x` executable permissions on POSIX systems
- **Cyberpunk ANSI Aesthetics**:
  - Modern ASCII art banner with dynamic terminal detection
  - Color-coded status indicators: Success, Error, Step, Info
  - Dynamic responsive terminal sizing and live progress tables

---

## Curated Tool Categories (65+ Tools)

### 1. OSINT & Reconnaissance
- **Sherlock** (`sherlock-project/sherlock`): Hunt down social media accounts across 400+ platforms
- **theHarvester** (`laramies/theHarvester`): Gather emails, names, subdomains, IPs from search engines
- **PhoneInfoga** (`sundowndev/phoneinfoga`): Advanced phone number OSINT framework
- **Holehe** (`megadose/holehe`): Email registered account checker for 120+ platforms
- **SpiderFoot** (`smicallef/spiderfoot`): Automated OSINT collection engine with hundreds of data modules
- **Seeker** (`thewhiteh4t/seeker`): High-precision smartphone geolocation social engineering
- **Nexfil** (`thewhiteh4t/nexfil`): Fast profile finder across 350+ sites in seconds
- **FinalRecon** (`thewhiteh4t/finalrecon`): All-in-one web reconnaissance engine (whois, headers, SSL, crawl)
- **Maigret** (`soxoj/maigret`): Collect dossier by username from 3000+ sites with URL validation
- **Recon-ng** (`lanmaster53/recon-ng`): Full-featured modular web reconnaissance framework
- **Sublist3r** (`aboul3la/Sublist3r`): Subdomain enumeration via search engines
- **GHunt** (`mxrch/GHunt`): Offensive Google account OSINT tool
- **Social-Analyzer** (`qeeqbox/social-analyzer`): Profile finder across 1000+ social networks
- **IP-Tracer** (`htr-tech/IP-Tracer`): Track IP location, ISP, country, ASN and coordinates
- **Infoga** (`m4ll0k/Infoga`): Email OSINT and PGP server harvester

### 2. Web Application Security & API Fuzzing
- **SQLMap** (`sqlmapproject/sqlmap`): Automatic SQL injection and database takeover engine
- **XSStrike** (`s0md3v/XSStrike`): Advanced XSS detection suite with intelligent fuzzing
- **Nuclei** (`projectdiscovery/nuclei`): Fast and customizable vulnerability scanner using YAML DSL
- **Subfinder** (`projectdiscovery/subfinder`): Fast passive subdomain enumeration
- **HTTPX** (`projectdiscovery/httpx`): Fast and multi-purpose HTTP probing toolkit
- **Katana** (`projectdiscovery/katana`): Next-generation web crawler and spider
- **FFUF** (`ffuf/ffuf`): Blazing fast web fuzzer for paths, vhosts, and parameters
- **Dalfox** (`hahwul/dalfox`): Parameter analysis and XSS scanner in Go
- **Commix** (`commixproject/commix`): Automated command injection exploiter
- **Arjun** (`s0md3v/Arjun`): HTTP parameter discovery suite (hidden GET/POST/JSON parameters)
- **Dirsearch** (`maurosoria/dirsearch`): Advanced multithreaded web path scanner
- **WhatWeb** (`urbanadventurer/WhatWeb`): Next generation web technologies and CMS identifier
- **CMSeeK** (`Tuhinshubhra/CMSeeK`): CMS detection and exploitation (WordPress, Joomla, Drupal, 170+ others)
- **ParamSpider** (`devanshbatham/paramspider`): Mining parameters from Web Archives for bug bounty
- **Wfuzz** (`xmendez/wfuzz`): Web application fuzzer and vulnerability assessment
- **Nikto** (`sullo/nikto`): Web server scanner for dangerous files and server flaws
- **XSpear** (`hahwul/XSpear`): Powerful XSS scanning and parameter analysis

### 3. Network Scanning & Enumeration
- **RustScan** (`RustScan/RustScan`): Modern port scanner - 65,000 ports in 3 seconds
- **Masscan** (`robertdavidgraham/masscan`): Internet-scale TCP port scanner
- **Netdiscover** (`alexxy/netdiscover`): Active/passive ARP reconnaissance
- **Bettercap** (`bettercap/bettercap`): Swiss Army knife for 802.11, BLE, IPv4/IPv6 MITM attacks
- **Responder** (`SpiderLabs/Responder`): LLMNR, NBT-NS and MDNS poisoner & credential harvester
- **Impacket** (`fortra/impacket`): Essential Python library for working with SMB, WMI, Kerberos
- **NetExec** (`Pennywiser-org/NetExec`): Active Directory & network exploitation suite (Modern CrackMapExec)
- **Sniffnet** (`GyulyV/sniffnet`): Modern cross-platform network traffic monitor

### 4. Wireless & IoT Security
- **Airgeddon** (`v1s1t0r1sh3r3/airgeddon`): Multi-use wireless network auditing script
- **Fluxion** (`FluxionNetwork/fluxion`): WPA/WPA2 social-engineering auditing research tool
- **Wifite2** (`derv82/wifite2`): Automated wireless auditor for WEP, WPA, WPS
- **EAPHammer** (`s0lst1c3/eaphammer`): Targeted evil twin attacks against WPA2-Enterprise
- **FakeAPBuilder** (`karthik558/FakeAPBuilder`): Rogue AP and captive portal builder for MITM

### 5. Exploitation, C2 & Payloads
- **Metasploit Framework** (`rapid7/metasploit-framework`): World-renowned penetration testing framework
- **Villain** (`t3l3machus/Villain`): Windows/Linux backdoor generator with sibling server multi-session
- **Sliver** (`BishopFox/sliver`): Cross-platform adversary emulation and Red Team C2
- **Havoc C2** (`HavocFramework/Havoc`): Modern malleable post-exploitation C2 framework
- **Routersploit** (`threat9/routersploit`): Embedded device and IoT router exploitation framework
- **PwnCat** (`calebstewart/pwncat`): Advanced reverse/bind shell handler with automated privesc
- **Red Python Scripts** (`davidbombal/red-python-scripts`): Curated offensive security scripts
- **MHDDoS** (`MatrixTM/MHDDoS`): DDoS stress testing framework with 36+ attack methods

### 6. Privilege Escalation & Pivoting
- **PEASS-ng** (`carlospolop/PEASS-ng`): LinPEAS and WinPEAS privilege escalation scripts
- **LinEnum** (`rebootuser/LinEnum`): Scripted Local Linux Enumeration & checks
- **Linux-Exploit-Suggester** (`The-Z-Labs/linux-exploit-suggester`): Kernel exploit suggester
- **Chisel** (`jpillora/chisel`): Fast TCP/UDP tunnel over HTTP via SSH
- **Ligolo-ng** (`nicocha30/ligolo-ng`): Lightweight pivoting tool using TUN interfaces
- **PayloadsAllTheThings** (`swisskyrepo/PayloadsAllTheThings`): Cheatsheets and bypass payloads

### 7. Password Cracking & Wordlists
- **SecLists** (`danielmiessler/SecLists`): Wordlists for fuzzing, discovery, and cracking
- **THC-Hydra** (`vanhauser-thc/thc-hydra`): High-speed network logon cracker
- **CeWL** (`digininja/CeWL`): Custom Word List Generator spidering websites

### 8. Forensics & Reverse Engineering
- **Volatility 3** (`volatilityfoundation/volatility3`): Memory forensics framework
- **Apktool** (`iBotPeaches/Apktool`): Reverse engineering Android APK files
- **JADX** (`skylot/jadx`): Dex to Java decompiler (CLI & GUI)

---

## Getting Started

### Installation & Launch

#### Linux / macOS
```bash
# 1. Clone this repository
git clone https://github.com/karthik558/setup_hack_env.git
cd setup_hack_env

# 2. Launch the interactive setup
python3 setup-hack.py
```

#### Windows (PowerShell / Windows Terminal / CMD)
```powershell
# 1. Clone this repository
git clone https://github.com/karthik558/setup_hack_env.git
cd setup_hack_env

# 2. Launch the interactive setup
python setup-hack.py
```

> **Privilege Note**:
> - **Linux/macOS**: Root (`sudo`) is **not** required for cloning tools into your user directory (`~/Tools`). The script will only request `sudo` when installing system packages via `apt`/`pacman`/`dnf`.
> - **Windows**: Run PowerShell or Windows Terminal as Administrator if you intend to install system packages via `winget` or `choco`. Otherwise, standard user permissions are fully supported for cloning and managing tools in `C:\Users\<user>\Tools`.

---

## Usage & CLI Options

You can run `setup-hack.py` interactively or pass command-line arguments for automated deployments:

```bash
# Launch rich interactive Cyberpunk menu
python3 setup-hack.py

# Update ALL installed tools in ~/Tools
python3 setup-hack.py --update

# Update tools in a custom directory
python3 setup-hack.py --update --dir /opt/security-tools

# Quick install ALL 65+ tools non-interactively
python3 setup-hack.py --all

# Install by category (e.g. OSINT and Web tools)
python3 setup-hack.py --category "osint,web"

# Install specific tools by name
python3 setup-hack.py --tools "sherlock,sqlmap,nuclei,subfinder"

# Specify custom destination directory
python3 setup-hack.py --dir /opt/tools --all

# List all available tools and their authentic upstream URLs
python3 setup-hack.py --list

# Install base Linux dependencies & prerequisites
python3 setup-hack.py --deps
```

### CLI Flag Reference

| Flag | Long Flag | Description |
|:---|:---|:---|
| `-a` | `--all` | Install all 65+ tools without interactive prompts |
| `-u` | `--update` | Update all installed repositories in destination folder |
| `-l` | `--list` | Inspect full catalog and upstream source URLs |
| `-d <dir>` | `--dir <dir>` | Set target folder for cloning tools (default: `~/Tools`) |
| `-c <cats>` | `--category <cats>` | Install tools by comma-separated categories |
| `-t <tools>`| `--tools <tools>` | Install tools by comma-separated names |
| | `--deps` | Install base Linux/macOS/Windows prerequisites, headers, and wordlists |
| | `--no-interactive` | Disable raw terminal mode for automated scripts / pipes |

---

## After-Installation System Tweaks (Optional)

1. **Extract rockyou wordlist manually** (if not already extracted by the script):
   ```bash
   sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
   ```

2. **Configure Proxychains with Tor**:
   ```bash
   sudo nano /etc/proxychains4.conf
   ```
   - Ensure `dynamic_chain` is uncommented and `strict_chain` is commented out.
   - Verify the bottom line points to:
     ```
     socks5 127.0.0.1 9050
     ```
   - Start the Tor service:
     ```bash
     sudo systemctl start tor
     ```

---

## Contributing

Contributions, issues, and tool recommendations are welcome! If you know of a stellar, active open-source security tool that should be included, open a Pull Request or Issue with the official upstream repository link.

## License

This project is licensed under the [MIT License](LICENSE).