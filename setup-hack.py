import os
import time
import subprocess
import datetime
import socket

# Colors for the terminal
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
VIOLET = '\033[0;35m'
CYAN = '\033[0;36m'
BLACK = '\033[0;30m'
NC = '\033[0m'  # No Color

# Let's start the script with a banner
def display_banner():

    banner =    "███████ ███████ ████████ ██    ██ ██████        ██   ██  █████   ██████ ██   ██\n"
    banner +=   "██      ██         ██    ██    ██ ██   ██       ██   ██ ██   ██ ██      ██  ██\n"
    banner +=   "███████ █████      ██    ██    ██ ██████  █████ ███████ ███████ ██      █████\n"
    banner +=        "██ ██         ██    ██    ██ ██            ██   ██ ██   ██ ██      ██  ██\n"
    banner +=   "███████ ███████    ██     ██████  ██            ██   ██ ██   ██  ██████ ██   ██\n"
    print(banner)
    
display_banner()

# Terminal header settings and information
print(f"{RED}Developer   :   KARTHIK LAL (https: // karthiklal.live){NC}")
print(f"{RED}Created Date:   2021-12-07{NC}")
print(f"{RED}Project     :   SETUP_HACK_ENV{NC}")
print(f"{RED}Purpose     :   Linux Dotfile{NC}")
print(f"{RED}Caution     :   This script will install all the necessary tools for hacking{NC}")
print()

# Abort the script if the user is not root
print("Checking if you are running this script on su mode or not")
if not os.geteuid() == 0:
    print(f"{RED}This script must be run as root{NC}")
    time.sleep(1)
    exit()
else:
    print(f"{GREEN}You are running this script on su mode{NC}")
    time.sleep(1)
    os.system("clear")

# Pulling the latest changes from the repository
print("{YELLOW}Fetching the repository and pulling the latest changes from the repository{NC}")
os.system("git fetch https://github.com/karthik558/setup_hack_env.git")
os.system("git pull https://github.com/karthik558/setup_hack_env.git")
time.sleep(1)
os.system("clear")

# Ask user for updating the system, if yes then update the system
print(f"{YELLOW}Do you want to update the system? (y/n){NC}")
update = input()
if update == "y":
    print(f"{YELLOW}Updating the system{NC}")
    os.system("apt update && apt upgrade -y")
    os.system("clear")
else:
    print(f"{YELLOW}Skipping the update{NC}")
    time.sleep(1)
    os.system("clear")

# Create a directory called tools on ~/ directory
print(f"{YELLOW}Creating a directory for clonning the tools and entering into it{NC}")
os.chdir("..")
os.makedirs("Tools", exist_ok=True)
os.chdir("Tools")
os.system("clear")

# Some linux dependencies for the tools to work
print(f"{YELLOW}Installing some linux dependencies{NC}")

# Terminal Emulator - Terminator
print(f"{YELLOW}Installing terminator terminal emulator{NC}")
os.system("apt install terminator -y")

# Tor proxy and other dependencies
print(f"{YELLOW}Installing tor browser and tor relay services{NC}")
os.system("apt install tor torbrowser-launcher -y")

os.system("apt install aptitude -y")
os.system("aptitude install libssl-dev bc -y")
os.system("apt install build-essential libssl-dev libffi-dev -y")
os.system("apt install libssl-dev libffi-dev build-essential -y")
os.system("apt install tar curl python3 python3-scapy network-manager -y")

# Python dependencies!]
print(f"{YELLOW}Installing some python dependencies{NC}")
os.system('apt install python3-venv -y')
os.system('apt install python3-all -y')
os.system('apt install python3-pip -y')
os.system('apt install python3-pip php php-cli -y')
os.system('apt install python3-pyqt5 hostapd -y')
os.system('python3 -m venv venv -y')
os.system('pip install pipenv -y')
os.system('python3 -m pip install --user pipenv -y')
os.system('pip install cloudscraper')

# System fetch and system information preview packages
print(f"{YELLOW}Installing htop and neofetch{NC}")
os.system("apt install htop neofetch -y")

# Metasploit Framework Dependencies
print(f"{YELLOW}Installing metasploit framework dependencies{NC}")
os.system('apt install zipalign apksigner -y')
os.system('wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool')
os.system('wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -O /usr/local/bin/apktool.jar')
# Lets make the apktool and apktool.jar executable
print(f"{YELLOW}Making the apktool and apktool.jar executable{NC}")
os.system('chmod +x /usr/local/bin/apktool')
os.system('chmod +x /usr/local/bin/apktool.jar')

# Unzip the wordlist from /usr/share/wordlists/rockyou.txt.gz
print(f"{YELLOW}Unzipping the wordlist from /usr/share/wordlists/rockyou.txt.gz{NC}")
os.system('gzip -d /usr/share/wordlists/rockyou.txt.gz')

# Enable VirtualEnv for python
print(f"{YELLOW}Enabling the virtual environment for python{NC}")
os.makedirs("~/.virtualvenv", exist_ok=True)
os.chdir(".virtualvenv")
os.system('python3 -m venv ~/.virtualenvs/')
os.system('source ~/.virtualenvs/bin/activate')
os.chdir('..')
print(f"{GREEN}Virtual environment has been enabled successfully{NC}")

# Telegram Desktop installation (optional)
print(f"{YELLOW}Do you want to install telegram desktop? (y/n){NC}")
telegram = input()
if telegram == "y":
    print(f"{YELLOW}Installing telegram desktop{NC}")
    os.system("apt install telegram-desktop -y")
else:
    print(f"{RED}Skipping the installation of telegram desktop{NC}")
    time.sleep(1)

# Clean and update the whole system after installing all the dependencies
os.system("apt clean -y && apt autoremove -y && apt update -y && apt upgrade -y && apt dist-upgrade -y")

# Let's start the installation of the tools now
print(f"{YELLOW} Starting the installation of tools{NC}")

# 1 - Phoneinfoga - Phone number information gathering & OSINT framework for phone numbers)
print(f"{RED}Do you want to install phoneinfoga? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing phoneinfoga{NC}")
    os.system('curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash')
    os.system('tar -xvf PhoneInfoga_Linux_x86_64.tar.gz')
    os.system('./phoneinfoga -h')
    os.system('mv phoneinfoga /usr/bin/phoneinfoga')
    print(f"{GREEN}Phoneinfoga has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of phoneinfoga{NC}")
    time.sleep(1)

# 2 - Scylla (The Simplistic Information Gathering Engine | Find Advanced Information on a Username, Website, Phone Number, etc.)
print(f"{RED}Do you want to install scylla? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing scylla{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/Scylla.git')
    os.chdir('Scylla')    
    os.system('python3 -m pip install -r requirments.txt')
    os.chdir('..')    
    print(f"{GREEN}Scylla has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of scylla{NC}")
    time.sleep(1)

# 3 - Seeker (Accurately Locate Smartphones using Social Engineering)
print(f"{RED}Do you want to install seeker? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing seeker{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/seeker.git')
    os.chdir('seeker')
    os.system('git pull https://github.com/thewhiteh4t/seeker')
    os.system('pip3 install requests')
    os.chdir('..')
    print(f"{GREEN}Seeker has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of seeker{NC}")
    time.sleep(1)

# 4 - Sherlock (Hunt down social media accounts by username across social networks)
print(f"{RED}Do you want to install sherlock? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing sherlock{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/sherlock.git')
    os.chdir('sherlock')
    os.system('git pull https://github.com/sherlock-project/sherlock.git')
    os.system('python3 -m pip install -r requirements.txt')
    os.chdir('..')
    print(f"{GREEN}Sherlock has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of sherlock{NC}")
    time.sleep(1)

# 5 - Nextfill (OSINT tool for finding profiles by username)
print(f"{RED}Do you want to install nextfill? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing nextfill{NC}")
    os.system('git clone https://github.com/thewhiteh4t/nexfil.git')
    os.chdir('nexfil')
    os.system('git pull https://github.com/thewhiteh4t/nexfil.git')
    #os.system('pip3 install -r requirements.txt')
    print(f"{YELLOW}Please run pip3 install -r requirements.txt manually{NC}")
    os.chdir('..')
    print(f"{GREEN}Nextfill has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of nextfill{NC}")
    time.sleep(1)

# 6 - Maryam Scanner (OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering.)
print(f"{RED}Do you want to install maryam scanner? (y/n){NC}")
if input() == "y":
    os.system('apt install maryam')
    print(f"{GREEN}Maryam scanner has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of maryam scanner{NC}")
    time.sleep(1)

# 7 - XSpear (Powerfull XSS Scanning and Parameter analysis tool)
print(f"{RED}Do you want to install xspear? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing xspear{NC}")
    os.system('git clone https://github.com/hahwul/XSpear.git')
    os.chdir('XSpear')
    os.system('gem install XSpear && gem install XSpear-1.4.1.gem')
    os.chdir('..')
    print(f"{GREEN}XSpear has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of xspear{NC}")
    time.sleep(1)

# 8 - SecList (SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more.)
print(f"{RED}Do you want to install seclist? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing seclist{NC}")
    os.system('apt install seclists -y')
    print(f"{GREEN}SecList has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of seclist{NC}")
    time.sleep(1)

# 9 - MHDDOS (Best DDoS Attack Script Python3, Cyber Attack With 36 Methods)
print(f"{RED}Do you want to install mhddos? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing mhddos{NC}")
    os.system('git clone https://github.com/MatrixTM/MHDDoS.git')
    os.chdir('MHDDoS')
    os.system('pip3 install -r requirements.txt')
    os.system('pip install git+https://github.com/MHProDev/PyRoxy.git --upgrade')
    os.chdir('..')
    print(f"{GREEN}MHDDOS has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of mhddos{NC}")
    time.sleep(1)

# 10 - SHARK (A shark is a tool that will help you do Phishing in an advanced way so no one checks and identify that you are doing phishing.
print(f"{RED}Do you want to install shark? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing shark{NC}")
    print(f"{RED}Keep your ngrok authtoken for installing shark{NC}")
    os.system(
        'wget -qO- https://github.com/Bhaviktutorials/shark/raw/master/setup | sudo bash')
    print(f"{GREEN}SHARK has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of shark{NC}")
    time.sleep(1)

# 11 - FakeAPBuilder (This project is a bash script that automates the creation of fake access points for MITM (Man-in-the-Middle) attacks.)
print(f"{RED}Do you want to install create fakeap-builder? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing mitm attack{NC}")
    os.system('apt install mdk3 -y')
    os.system('git clone https://github.com/karthik558/FakeAPBuilder.git')
    print(f"{GREEN}MITM Attack has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of mitm attack{NC}")
    time.sleep(1)

# 12 - Netdiscover (Netdiscover is a tool for discovering hosts on a local area network. It uses ARP requests to find out which hosts are up and which IP addresses they have.)
print(f"{RED}Do you want to install netdiscover? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing netdiscover{NC}")
    os.system('apt install netdiscover -y')
    print(f"{GREEN}Netdiscover has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of netdiscover{NC}")
    time.sleep(1)

# 13 - UPI-OSINT (This tool is used to find the name of the bank and the bank account holder's name from the UPI ID.)
print(f"{RED}Do you want to install upi-int? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing upi-int{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/UPI-INT.git')
    os.chdir('UPI-INT')
    os.system('git pull https://github.com/BiswajeetRay7/UPI-INT')
    print(f"{YELLOW}Installing Nodejs{NC}")
    os.system('apt install nodejs -y')
    print(f"{YELLOW}Installing npm{NC}")
    os.system('apt install npm -y')
    print(f"{YELLOW}Installing npm-axios{NC}")
    os.system('npm install axios')
    print(f"{YELLOW}Installing npm-bluebird{NC}")
    os.system('npm install bluebird')
    os.chdir('..')
    print(f"{GREEN}UPI-OSINT has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of upi-int{NC}")
    time.sleep(1)

# 14 - Track-IP (Track-IP is a tool that allows you to track the location of an IP address.)
print(f"{RED}Do you want to install track-ip? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing track-ip{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/track-ip.git')
    os.chdir('track-ip')    
    os.system('git pull https://github.com/htr-tech/track-ip')
    os.chdir('..')
    print(f"{GREEN}Track-IP has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of track-ip{NC}")
    time.sleep(1)

# 15 - Holehe (Holehe is a tool that allows you to find the email address of a person using their username on different platforms.)
print(f"{RED}Do you want to install holehe? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing holehe{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/holehe')
    os.chdir('holehe')
    os.system('git pull https://github.com/megadose/holehe')
    os.system('python3 setup.py install')
    os.chdir('..')
    print(f"{GREEN}Holehe has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of holehe{NC}")
    time.sleep(1)

# 16 - Fluxion (Fluxion is a tool that allows you to hack wifi networks.)
print(f"{RED}Do you want to install fluxion? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing fluxion{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/fluxion.git')
    os.chdir('fluxion')
    os.system('git pull https://github.com/FluxionNetwork/fluxion')
    os.system('chmod +x fluxion.sh')
    os.chdir('..')
    print(f"{GREEN}Fluxion has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of fluxion{NC}")
    time.sleep(1)

# 17 - David-Bombal Scanner and Exploiter (David-Bombal script is very useful for performing various types of attacks on a target machine)
print(f"{RED}Do you want to install david-bombal scanner and exploiter scripts? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing david-bombal scanner and exploiter scripts{NC}")
    os.system('git clone https://github.com/Ethical-Hacking-Tools/red-python-scripts.git')
    os.chdir('red-python-scripts')
    os.system('git pull https://github.com/davidbombal/red-python-scripts.git')
    os.chdir('..')
    print(f"{GREEN}David-Bombal Scanner and Exploiter has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of david-bombal scanner and exploiter scripts{NC}")
    time.sleep(1)

# 18 - Villain Tool is a Windows & Linux backdoor generator and multi-session handler that allows users to connect with sibling servers(other machines running Villain) and share their backdoor sessions, handy for working as a team.)
print(f"{RED}Do you want to install villain? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing villain{NC}")
    os.system('git clone https://github.com/t3l3machus/Villain.git')
    os.chdir('Villain')
    os.system('pip3 install -r requirements.txt')
    os.chdir('..')
    print(f"{GREEN}Villain has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of villain{NC}")
    time.sleep(1)

# 19 - TrucallerJS (This is a library for retrieving phone number details using the Truecaller API.)
print(f"{RED}Do you want to install TrucallerJS? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing TrucallerJS{NC}")
    os.system('git clone https://github.com/sumithemmadi/truecallerjs.git')
    os.chdir('truecallerjs')
    os.system('npm install truecallerjs')
    os.system('npm install -g truecallerjs')    
    os.chdir('..')
    print(f"{GREEN}TrucallerJS has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of TrucallerJS{NC}")
    time.sleep(1)
    
# 20 - Volatility (Volatility is a memory forensics framework for incident response and malware analysis.)
print(f"{RED}Do you want to install volatility? (y/n){NC}")
if input() == "y":
    print(f"{YELLOW}Installing volatility{NC}")
    os.system('git clone https://github.com/volatilityfoundation/volatility3.git')
    os.chdir('volatility3')    
    os.system('python3 setup.py build')
    os.system('python3 setup.py install')
    os.system('pip3 install -r requirements.txt')
    os.chdir('..')
    print(f"{GREEN}Volatility has been installed successfully{NC}")
else:
    print(f"{RED}Skipping the installation of volatility{NC}")
    time.sleep(1)
    
# Lets update the clean and update the system once again
os.system('apt update -y && apt upgrade -y && apt autoremove -y && apt autoclean -y')

# Clear the screen
os.system('clear')

# Print installation complete message
hostname = socket.gethostname()
# Get the current time
now = datetime.datetime.now()
hour = now.hour
if hour >= 4 and hour < 12:
    print(f"Good Morning {hostname},Installation is complete")
elif hour >= 12 and hour < 17:
    print(f"Good Afternoon {hostname},Installation is complete")
elif hour >= 17 and hour < 20:
    print(f"Good Evening {hostname},Installation is complete")
else:
    print(f"Good Night {hostname},Installation is complete")
    time.sleep(2)

# Let's start the scrzipt with a banner
def display_banner():
    
    banner =    "███████ ████████  █████  ██████  ████████       ██   ██  █████   ██████ ██   ██ ██ ███    ██  ██████\n"
    banner +=   "██         ██    ██   ██ ██   ██    ██          ██   ██ ██   ██ ██      ██  ██  ██ ████   ██ ██\n"
    banner +=   "███████    ██    ███████ ██████     ██    █████ ███████ ███████ ██      █████   ██ ██ ██  ██ ██   ███\n"
    banner +=        "██    ██    ██   ██ ██   ██    ██          ██   ██ ██   ██ ██      ██  ██  ██ ██  ██ ██ ██    ██\n"
    banner +=   "███████    ██    ██   ██ ██   ██    ██          ██   ██ ██   ██  ██████ ██   ██ ██ ██   ████  ██████ \n"
    print(banner)

display_banner()

# Press enter to exit
print(f"{GREEN}Press enter to exit{NC}")
