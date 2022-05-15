# TP-LINL-WN722N RUN SCRIPT
# COPYRIGHT: GPL-3.0-or-later
# AUTHOR: KARTHIK LAL
# DATE:   07.11.2021
# CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX DISTRIBUTION
# TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
# USE AT YOUR OWN RISK.
# LICESNSE: GNU GENERAL PUBLIC LICENSE V3.0
# OPENSOURCE SOFTWARE LICENSE AGREEMENT FOR KALI LINUX DISTRIBUTION
# https://www.gnu.org/licenses/gpl-3.0.en.html
# HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.
#
#!/bin/bash
# Path: TP-LINK DRIVER\TP-LINK-WN722N(1).sh
# Abort if its not running on root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Abort if not running on Kali Linux
if [[ ! -e /etc/apt/sources.list.d/kali-linux.list ]]; then
   echo "This script must be run on Kali Linux" 1>&2
   exit 1
fi

# Welcome Welcome Message
echo "Welcome to TP-LINK DRIVER run script 2"

# Let's start 
# Update the system and upgrade the packages
apt update && apt upgrade &&  apt install bc && apt-get install build-essential && apt-get install libelf-dev

# check if the folder exists or not 
if [ ! -d "./rtl8188eus" ]; then
   echo "Cloning the driver from github"
   git clone https://github.com/aircrack-ng/rtl8188eus && cd rtl8188eus
else 
   echo "Driver already cloned"
fi

# Lets start compiling the driver
echo "Compiling the driver"
echo "This may take some time"
make && make install

# Reboot the system
echo "2nd script is done. Rebooting the system"
echo "Do you want to reboot now ? (y/n)"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   echo "Rebooting KALI Now"
   reboot
else
   echo "You can reboot later"
fi

## NOTE/CAUTION:
# Blacklist the old driver ( if you have one )
#sudo -i echo "blacklist r8188eu" > "/etc/modprobe.d/realtek.conf"
#sudo modprobe 8188eu (do this incase you have the old driver)