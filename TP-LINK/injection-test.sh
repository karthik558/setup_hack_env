#!/bin/bash

# Banner for the script
# ██╗████████╗███████╗███████╗████████╗
# ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
# ██║   ██║   █████╗  ███████╗   ██║   
# ██║   ██║   ██╔══╝  ╚════██║   ██║   
# ██║   ██║   ███████╗███████║   ██║   
# ╚═╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝   

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
   printf "${RED} This script must be run as root ${NC}" 1>&2
   exit 1
fi

# Abort if not running on Kali Linux
if [[ ! -e /etc/apt/sources.list.d/kali-linux.list ]]; then
   printf "${RED}This script must be run on Kali Linux ${NC}" 1>&2
   exit 1
fi

# Ask user if they want update and upgrade the system before testing the injection
printf "${YELLOW}Do you want to update and upgrade the system before testing the injection? [Y/n] ${NC}"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${YELLOW}Your KALI LINUX is now UPDATING.. & UPGRADING..${NC}"
   echo -ne '/\/\          (20%)\r'
   sleep 0
   echo -ne '/\/\/\/\        (40%)\r'
   sleep 1
   echo -ne '/\/\/\/\/\/\      (60%)\r'
   sleep 3
   echo -ne '/\/\/\/\/\/\/\/\      (80%)\r'
   sleep 4
   echo -ne '/\/\/\/\/\/\/\/\/\/\   (100%)\r'
   echo -ne '\n'
   apt-get update && apt-get upgrade -y
else 
   printf "${RED}Skipping update and upgrade ${NC}"
fi

# Lets start the injection test
printf "${YELLOW}Select the correct interface to test packet-injection ! (0/1) ${NC}"
read -r answer
if [[ $answer == 0 ]]; then
   printf "${RED}Starting the injection test on WLAN0... ${NC}"
   ifconfig wlan0 down
   iwconfig wlan0 mode monitor
   ifconfig wlan0 up
   iwconfig wlan0
   printf "${GREEN}Injecting packets on interface 0 ${NC}"
   aireplay-ng --test wlan0
   printf "${GREEN}Packet injection test done on interface 0 and its working fine ${NC}"
else
   printf "${RED}Starting the injection test on WLAN1... ${NC}"
   ifconfig wlan1 down
   iwconfig wlan1 mode monitor
   ifconfig wlan1 up
   iwconfig wlan1
   printf "${GREEN}Injecting packets on interface 1 ${NC}"
   aireplay-ng --test wlan1
   printf "${GREEN}Packet injection test done on interface 1 and its working fine ${NC}"
fi

##
## Brief about this script >>.
## Author/Developer Information >>.
## License Information >>.
##
# ├── KALI DESKTOP ENVIRONMENT SETUP SCRIPT
# ├── AUTHOR: KARTHIK LAL (https://github.com/karthik558) (https://karthiklal.live)
# ├── DATE:   07.11.2021
# ├── CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX DISTRIBUTION
# ├── TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
# ├── USE AT YOUR OWN RISK.
# ├── LICENSE: GNU GENERAL PUBLIC LICENSE V3.0
# ├── OPENSOURCE SOFTWARE LICENSE AGREEMENT FOR KALI LINUX DISTRIBUTION
# ├── https://www.gnu.org/licenses/gpl-3.0.en.html
# └── HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.
##
## Script Information >>.
##
# ├── This script is used to test the injection capability of the wireless card.
# ├── It will try to inject a packet on channel 0 and channel 1.
# └── If the packet is received, the injection is working.
# └── If the packet is not received, the injection is not working.
# └── This script is only for Kali Linux.
# └── This script is only for TP-Link TL-WN722N V1 and V2.
# └── Default interface set to 0 // change this accoding to you pc
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