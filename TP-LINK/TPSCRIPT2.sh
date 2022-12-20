#!/bin/bash

# Banner for the script
# 88888888888 8888888b.       888      8888888 888b    888 888    d8P
#     888     888   Y88b      888        888   8888b   888 888   d8P
#     888     888    888      888        888   88888b  888 888  d8P
#     888     888   d88P      888        888   888Y88b 888 888d88K
#     888     8888888P"       888        888   888 Y88b888 8888888b
#     888     888      888888 888        888   888  Y88888 888  Y88b
#     888     888             888        888   888   Y8888 888   Y88b
#     888     888             88888888 8888888 888    Y888 888    Y88b

# Select the color of the text in the terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
VIOLET='\033[0;35m'
CYAN='\033[0;36m'
BLACK='\033[0;30m'
NC='\033[0m' # No Color

# Abort if its not running on root
if [[ $EUID -ne 0 ]]; then
   printf "${RED}This script must be run as root ${NC}" 1>&2
   exit 1
fi

# Abort if not running on Kali Linux or ParrotOS
# echo "Checking if you are running this script on Kali Linux or ParrotOS"
# if [[ -f /etc/os-release ]]; then
#    . /etc/os-release
#    OS=$NAME
#    VER=$VERSION_ID
#    if [[ $OS == "Kali GNU/Linux" ]]; then
#       printf "${GREEN}You are running this script on Kali Linux${NC}\n"
#       sleep 1
#       clear
#    elif [[ $OS == "Parrot GNU/Linux" ]]; then
#       printf "${GREEN}You are running this script on Parrot OS${NC}\n"
#       sleep 1
#       clear
#    else
#       printf "${RED}You are not running this script on Kali Linux or Parrot OS${NC}\n"
#       sleep 1
#       exit
#    fi

# Let's start
# Update the system and upgrade the packages
printf "${YELLOW}Welcome back %USER${NC}"
printf "${RED}Updating the system and upgrading the packages... ${NC}"
apt update && apt upgrade && apt install bc && apt-get install build-essential && apt-get install libelf-dev
printf "${GREEN}Done! ${NC}"

# Check if the folder exists or not if not clone the repo from github
printf "${RED}Checking if the folder exists or not... ${NC}"
if [ ! -d "./rtl8188eus" ]; then
   printf "${RED}Cloning the repo from github... ${NC}"
   git clone
   git clone https://github.com/karthik558/rtl8188eus && cd rtl8188eus
   printf "${GREEN}Clonning Done! ${NC}"
else
   printf "${GREEN}Folder already exists! ${NC}"
   sleep 1
fi

# Get into the directory first to compile driver
printf "${YELLOW}Lets get into the directory... ${NC}"
cd rtl8188eus

# Lets start compiling the driver
printf "${RED}Compiling the driver... ${NC}"
printf "${RED}This will take some time... ${NC}"
make && make install
printf "${GREEN}Compiling driver done! ${NC}"

# Lets reboot and check if the driver is working or not by running the injection-test.sh script from the TP-LINK folder in this repo
printf "${YELLOW}Done installing TPLINK2.sh ${NC}"
printf "${YELLOW}REBOOT SYSTEM NOW [RECOMMENDED TO RESTART] [y/n] ${NC}"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${GREEN}Rebooting the system... ${NC}"
   clear
   printf "${GREEN}HAPPY HACKING PEOPLES.....${NC}"
   reboot
else
   printf "${RED}Reboot request aborted by %USER ${NC}"
   printf "${RED}Exiting the script... ${NC}"
   clear
   printf "${GREEN}HAPPY HACKING PEOPLES.....${NC}"
   exit 1
fi

##
## Brief about this script >>.
## Author/Developer Information >>.
## License Information >>.
##
# ├── TPLINK 722N Driver Installation Script 2 of 2 (TPSCRIPT2.sh)
# ├── AUTHOR: KARTHIK LAL (https://github.com/karthik558) (https://karthiklal.live)
# ├── DATE:   07.11.2021
# ├── CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX AND PARROTOS DISTRIBUTION
# ├── TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
# ├── USE AT YOUR OWN RISK.
# └── HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.
##
## Script Information >>.
##
# ├── This script is for installing the TP-LINK-WN722N driver on Kali Linux and ParrotOS.
# └── This driver is directly taken from the aircrack-ng github repository.
##
## Script Liscence >>.
##
## This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
## You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
##
## Script Declaration >>.
##
# ├── THANKS FOR USING THIS SCRIPT.
# ├── WE ARE HAPPY TO HAVE YOU ON OUR TEAM.
# ├── WE ARE ALWAYS HERE TO HELP YOU (JUST RAISE A ISSUE ON GITHUB IF YOU HAVE ISSUE WITH THIS SCRIPT).
# ├── THIS CODE IS WRITTEN BY : KARTHIK LAL (karthiklal@duck.com/karthiklal.live)
# ├── WEBSITE : https://karthiklal.live
# ├── EMAIL : karthik.lal558@gmail.com/karthiklal@duck.com
# ├── GITHUB : karthik558
# └── CONTRIBUTIONS ARE WELCOME. :)
##
##
