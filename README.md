# Setup Hack Environment (Cross-Platform: Windows, macOS, Linux)

An advanced, enterprise-grade ethical hacking and penetration testing environment automated installer. Fully cross-platform, supporting **Windows 10/11**, **macOS** (Apple Silicon & Intel), and **all Linux distributions** (Kali Linux, Parrot OS, Debian, Ubuntu, Arch Linux, Manjaro, BlackArch, Fedora, RHEL, CentOS, openSUSE, Alpine Linux, etc.).

Curated with **65+ top-tier cybersecurity tools** fetched directly from their **authentic upstream sources** (ProjectDiscovery, SQLMapProject, Sherlock-Project, Rapid7, and more).

Includes an **interactive terminal checkbox selector with live fuzzy search filtering**, **role-based installation presets**, **isolated virtual environments per tool**, a **pre-flight system doctor**, **disk space manager & cache cleaner**, **JSON configuration export/import**, and **containerized Docker support**.

![Banner](assets/script-linux.png)

---

## Key Highlights & Enterprise Architecture

- **Full Cross-Platform Support**:
  - **Linux (All Distros)**: Native support for Debian/Kali/Parrot (`apt`), Arch/Manjaro/BlackArch (`pacman`), Fedora/RHEL/CentOS (`dnf`/`yum`), openSUSE (`zypper`), and Alpine (`apk`).
  - **macOS**: Native support on Apple Silicon (M1/M2/M3/M4) & Intel with Homebrew integration.
  - **Windows**: Native support on Windows 10/11 (PowerShell / Windows Terminal / CMD) with `winget`/`choco` support and `msvcrt` raw key capture.
- **100% Authentic Upstream Sources**: No third-party forks or obsolete organizations. Every tool is cloned directly from its official creators and foundations.
- **Role-Based Profiles & Presets**: One-click curated bundles for Bug Bounty, OSINT, Red Teaming, Network Auditing, Wireless, Forensics, or Minimal starter setups.
- **Isolated Virtual Environments (.venv)**: Every Python tool receives its own isolated virtual environment to prevent dependency conflicts (PEP 668 compliant), with auto-generated portable launcher wrappers (`run.sh` / `run.bat`).
- **Interactive Checkbox UI with Live Search**:
  - Press `[/]` to instantly filter tools by name, category, or description in real time
  - `[Up/Down]` or `[k/j]` Navigate smoothly across all tools (works on Windows, macOS, Linux)
  - `[Space]` Toggle tool selection [X] / [ ]
  - `[a]` Select / Deselect all visible tools in active search filter
  - `[c]` Toggle entire category of the focused tool
  - `[d]` Change destination directory on the fly
  - `[Enter]` Start batch installation
- **Pre-Flight Environment Doctor**: Audits compilers (Go, Rust, Node, Ruby, GCC, Make), Git, Python, Docker, system packages, storage headroom, and tests live TLS connection latency to GitHub and PyPI.
- **Storage Manager & Disk Cleaner**: Inspects tool disk usage, ranks largest tools, and provides a safe one-key cache purger for Python bytecode (`__pycache__`), test caches, and git garbage collection (`git gc`).
- **Configuration Export & Import**: Generates reproducible JSON manifests containing exact tool lists, git commit hashes, branches, and platform metadata for team sync and dotfiles.
- **Containerized Docker Sandbox**: Ships with production Kali Linux `Dockerfile` and `docker-compose.yml` for isolated operations with persistent host volume mounting.
- **Smart Git Auto-Updater**:
  - Automatically scans your tools folder (`~/Tools` or custom directory)
  - Runs `git pull` across all installed repositories
  - Reports branch, commit status, and updates dependencies inside isolated `.venv` environments.

---

## Role-Based Profiles & Presets

Instead of manually picking tools or cloning everything, you can deploy role-tailored security suites using the interactive menu or the `--profile` flag:

| Profile ID | Role Name | Included Tools Highlights |
|:---|:---|:---|
| `bug-bounty` | Bug Bounty & Web Hunter | SQLMap, XSStrike, Nuclei, Subfinder, HTTPX, Katana, FFUF, Dalfox, Commix, Arjun, Dirsearch, WhatWeb, CMSeeK, ParamSpider, Wfuzz, Nikto, Sublist3r, SecLists, PayloadsAllTheThings |
| `osint` | OSINT & Digital Intelligence | Sherlock, theHarvester, PhoneInfoga, Holehe, SpiderFoot, Seeker, Nexfil, FinalRecon, Maigret, Recon-ng, Sublist3r, GHunt, Social-Analyzer, IP-Tracer, Infoga |
| `red-team` | Red Team & Exploitation | Metasploit-Framework, Sliver, Havoc-C2, Villain, Impacket, Responder, NetExec, PwnCat, Routersploit, PEASS-ng, LinEnum, Linux-Exploit-Suggester, Chisel, Ligolo-ng, PayloadsAllTheThings |
| `network` | Network & Infrastructure | RustScan, Masscan, Netdiscover, Bettercap, Responder, Impacket, NetExec, Sniffnet, THC-Hydra |
| `wireless` | Wireless & WiFi Auditing | Airgeddon, Fluxion, Wifite2, EAPHammer, FakeAPBuilder |
| `forensics` | Forensics & Reverse Engineering | Volatility3, Apktool, JADX, Linux-Exploit-Suggester, PEASS-ng |
| `essential` | Essential Starter Kit | Sherlock, theHarvester, SQLMap, Nuclei, Subfinder, HTTPX, FFUF, Dirsearch, RustScan, Bettercap, Responder, Impacket, SecLists, THC-Hydra, PEASS-ng |

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

# 2. Launch the interactive menu
python3 setup-hack.py
```

#### Windows (PowerShell / Windows Terminal / CMD)
```powershell
# 1. Clone this repository
git clone https://github.com/karthik558/setup_hack_env.git
cd setup_hack_env

# 2. Launch the interactive menu
python setup-hack.py
```

#### Docker Container Sandbox
Run tools in an isolated Kali Linux container without modifying your host system:
```bash
# Build and run interactive session
docker-compose run --rm setup-hack

# Or run a specific profile directly in Docker
docker-compose run --rm setup-hack --profile bug-bounty
```

> **Privilege Note**:
> - **Linux/macOS**: Root (`sudo`) is **not** required for cloning tools into your user directory (`~/Tools`). The script will only request `sudo` when installing system packages via `apt`/`pacman`/`dnf`.
> - **Windows**: Run PowerShell or Windows Terminal as Administrator if you intend to install system packages via `winget` or `choco`. Otherwise, standard user permissions are fully supported for cloning and managing tools in `C:\Users\<user>\Tools`.

---

## Usage & CLI Commands

You can run `setup-hack.py` interactively or pass command-line arguments for automated deployments:

```bash
# Launch interactive Cyberpunk menu
python3 setup-hack.py

# Pre-flight environment diagnostics and compiler checks
python3 setup-hack.py --doctor

# Install a specific role profile (e.g. bug-bounty or osint)
python3 setup-hack.py --profile bug-bounty
python3 setup-hack.py --profile osint

# List all available role presets and included tools
python3 setup-hack.py --list-profiles

# Inspect tool disk footprint and storage metrics
python3 setup-hack.py --storage

# Purge Python bytecode, build caches, and optimize git repositories
python3 setup-hack.py --clean

# Export current installation state to reproducible JSON manifest
python3 setup-hack.py --export setup-manifest.json

# Import and replicate environment from JSON manifest
python3 setup-hack.py --import setup-manifest.json

# Update ALL installed tools in ~/Tools
python3 setup-hack.py --update

# Update tools in a custom directory
python3 setup-hack.py --update --dir /opt/security-tools

# Quick install ALL tools non-interactively
python3 setup-hack.py --all

# Install by category (e.g. OSINT and Web tools)
python3 setup-hack.py --category "osint,web"

# Install specific tools by name
python3 setup-hack.py --tools "sherlock,sqlmap,nuclei,subfinder"

# Specify custom destination directory
python3 setup-hack.py --dir /opt/tools --all

# List all available tools and official upstream repositories
python3 setup-hack.py --list

# Install base Linux dependencies & prerequisites
python3 setup-hack.py --deps
```

### CLI Flag Reference

| Flag | Long Flag | Description |
|:---|:---|:---|
| `-p <name>` | `--profile <name>` | Install tools from a role profile (`bug-bounty`, `osint`, `red-team`, `network`, `wireless`, `forensics`, `essential`) |
| | `--list-profiles` | List all available preset profiles and included tools |
| | `--doctor` | Run pre-flight environment diagnostics, compiler audits, and network latency tests |
| | `--storage` | Inspect disk footprint and storage metrics of installed tools |
| | `--clean` | Purge Python bytecode (`__pycache__`), caches, and optimize git repos with `git gc` |
| | `--export [file]` | Export installed tools manifest JSON |
| | `--import <file>` | Import and install tools from manifest JSON |
| | `--docker` | Manage or launch containerized Docker sandbox environment |
| | `--venv` | Enable isolated Python virtual environments per tool (default: enabled) |
| | `--no-venv` | Disable isolated virtual environments, use global Python interpreter |
| `-a` | `--all` | Install all tools without interactive prompts |
| `-u` | `--update` | Update all installed repositories in destination folder |
| `-l` | `--list` | Inspect full catalog and upstream source URLs |
| `-d <dir>` | `--dir <dir>` | Set target folder for cloning tools (default: `~/Tools`) |
| `-c <cats>` | `--category <cats>` | Install tools by comma-separated categories |
| `-t <tools>`| `--tools <tools>` | Install tools by comma-separated names |
| | `--deps` | Install base Linux/macOS/Windows prerequisites, headers, and wordlists |
| | `--no-interactive` | Disable raw terminal mode for automated scripts / pipes |

---

## Isolated Python Virtual Environments

Modern operating systems (e.g. Debian 12+, Ubuntu 23+, macOS Homebrew, Arch Linux) enforce PEP 668 ("externally managed environment"), preventing global `pip install` commands from interfering with system packages. Installing multiple security tools into a single global environment frequently leads to conflicting dependency versions (e.g., conflicting `urllib3`, `requests`, `cryptography`, or `pydantic` versions).

`setup_hack_env` solves this natively:
1. **Isolated `.venv` Per Tool**: Each Python tool receives its own isolated virtual environment inside its cloned directory (`<tool>/.venv`).
2. **Auto-Generated Launchers**: Every installed tool automatically receives an executable wrapper script:
   - On Linux/macOS: `<tool>/run.sh`
   - On Windows: `<tool>\run.bat`
   Running `./run.sh` automatically routes execution through that tool's specific `.venv` interpreter without manual activation.
3. **Toggleable**: To install into the active interpreter instead, simply pass `--no-venv`.

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

Contributions, issues, and tool recommendations are welcome! If you know of an active open-source security tool that should be included, open a Pull Request or Issue with the official upstream repository link.

## License

This project is licensed under the [MIT License](LICENSE).