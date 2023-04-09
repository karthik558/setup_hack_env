import os
import socket
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

# Lets start installing the driver
hostname = socket.gethostname()
print(f"{YELLOW}Welcome back {hostname}{NC}")
print(f"{YELLOW}Updating system and installing some dependencies for compiling rtl8188 driver into kernel{NC}")
os.system("apt update && apt upgrade && apt install bc && apt-get install build-essential && apt-get install libelf-dev")
print(f"{GREEN}Done{NC}")

# Check if the folder exists or not if not then clone the driver from github
print(f"{YELLOW}Checking if the driver folder exists or not{NC}")
if not os.path.isdir("./rtl8188eus"):
    print(f"{RED}Cloning the repo from github... {NC}")
    os.system("git clone https://github.com/karthik558/rtl8188eus && cd rtl8188eus")
    print(f"{GREEN}Cloning Done! {NC}")
else:
    print(f"{GREEN}Folder already exists! {NC}")
    time.sleep(1)

# Let compile the driver
print(f"{YELLOW}Compiling the driver{NC}")
os.system("cd rtl8188eus && make && make install")
print(f"{GREEN}Done{NC}")

# Prompt the user to reboot the system or not
print(f"{YELLOW}Do you want to reboot the system now? [y/n]{NC}")
answer = input()
if answer == "y":
    print(f"{GREEN}Rebooting the system{NC}")
    os.system("sudo -i reboot")
else:
    print(f"{GREEN}Reboot the system manually{NC}")
    exit()
