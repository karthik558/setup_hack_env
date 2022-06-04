#!/bin/bash

# Abort if its not running on root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Abort if not running on Kali Linux
# if [[ ! -e /etc/apt/sources.list.d/kali-linux.list ]]; then
#   echo "This script must be run on Kali Linux" 1>&2
#   exit 1
# fi

# Let's start
# 1 Dependencies for running this before installing
apt update && apt upgrade &&  apt install bc && apt-get install build-essential && apt-get install libelf-dev

# 2 Install Linux-Headers for compiling kernel
apt install linux-headers-$(uname -r)

# 3 Install DKMS and rmod the old driver
apt install dkms && sudo rmmod r8188eu.ko

# 4 CLone the driver from github
git clone https://github.com/aircrack-ng/rtl8188eus && cd rtl8188eus

# 5 Blacklist the old driver ( if you have one )
sudo -i echo "blacklist r8188eu" > "/etc/modprobe.d/realtek.conf"

# 6 Compile the driver and install it (after rebooting kali-linux)
echo "Cloning and black listing old driver is done."
echo "Now restarting Kali Linux and compiling the driver."

echo "Do you want to reboot now ? (y/n)"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   echo "Rebooting KALI Now"
   echo "run 2nd script after reboot"
   reboot
else
   echo "You can reboot later"
fi

##
## TP-LINL-WN722N RUN SCRIPT
## COPYRIGHT: GPL-3.0-or-later
## AUTHOR: KARTHIK LAL
## DATE:   07.11.2021
## CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX DISTRIBUTION
## TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
## USE AT YOUR OWN RISK.
## LICESNSE: GNU GENERAL PUBLIC LICENSE V3.0
## OPENSOURCE SOFTWARE LICENSE AGREEMENT FOR KALI LINUX DISTRIBUTION
## https://www.gnu.org/licenses/gpl-3.0.en.html
## HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.
##