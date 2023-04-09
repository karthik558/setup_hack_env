import os
import time

# Let's start the script with a banner
def display_banner():
    banner =   "███████████ ███████████             █████       █████ ██████   █████ █████   ████ \n"
    banner +=  "░█░░░███░░░█░░███░░░░░███           ░░███       ░░███ ░░██████ ░░███ ░░███   ███░\n"
    banner +=  "░   ░███  ░  ░███    ░███            ░███        ░███  ░███░███ ░███  ░███  ███\n"
    banner +=      "░███     ░██████████  ██████████ ░███        ░███  ░███░░███░███  ░███████\n"
    banner +=      "░███     ░███░░░░░░  ░░░░░░░░░░  ░███        ░███  ░███ ░░██████  ░███░░███\n"
    banner +=      "░███     ░███                    ░███      █ ░███  ░███  ░░█████  ░███ ░░███\n"
    banner +=      "█████    █████                   ███████████ █████ █████  ░░█████ █████ ░░████\n"
    banner +=      "░░░░░    ░░░░░                   ░░░░░░░░░░░ ░░░░░ ░░░░░    ░░░░░ ░░░░░   ░░░░ \n"
    print(banner)
    
display_banner()

# Select the color of the text in the terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
VIOLET='\033[0;35m'
CYAN='\033[0;36m'
BLACK='\033[0;30m'
NC='\033[0m' # No Color

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

# Lets start installing the dependencies
print(f"{YELLOW}Installing the dependencies{NC}")
os.system("apt update -y && apt upgrade -y && apt install bc -y && apt-get install build-essential -y && apt-get install libelf-dev -y")
print(f"{GREEN}Dependencies installed{NC}")

# Installing Linux Headers
print(f"{YELLOW}Installing Linux Headers{NC}")
os.system("apt-get install linux-headers-$(uname -r) -y")
print(f"{GREEN}Linux Headers installed{NC}")

# Installing DKMS and rmmod the old driver
print(f"{YELLOW}Installing DKMS and rmmod the old driver{NC}")
os.system("apt-get install dkms -y && rmmod r8188eu.ko")
print(f"{GREEN}DKMS and rmmod the old driver installed{NC}")

# Clone the driver from github
print(f"{YELLOW}Cloning the driver from github{NC}")
os.system("git clone https://github.com/karthik558/rtl8188eus")
print(f"{GREEN}Driver cloned{NC}")

# Blacklist the old driver
print(f"{YELLOW}Blacklisting the old driver{NC}")
os.system('sudo -i echo "blacklist r8188eu" >"/etc/modprobe.d/realtek.conf"')
print(f"{GREEN}Old driver blacklisted{NC}")

# Inform the user to reboot the system and run the script 2nd script to install the driver
print(f"{YELLOW}Reboot the system and run the 2nd script to install the driver{NC}")

# Prompt the user to reboot the system or not
print(f"{YELLOW}Do you want to reboot the system now? [y/n]{NC}")
answer = input()
if answer == "y":
  print(f"{GREEN}Rebooting the system{NC}")
  os.system("sudo -i reboot")
else:
  print(f"{GREEN}Reboot the system manually{NC}")
  exit()