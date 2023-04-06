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

# Ask user if they want update and upgrade the system before testing the injection
printf "${YELLOW}Do you want to update and upgrade the system before testing the injection? [Y/n] ${NC}"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${YELLOW}Your %DISTRO is now UPDATING.. & UPGRADING..${NC}"
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