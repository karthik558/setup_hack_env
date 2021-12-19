# Wifi Adapter Driver for Linux 
# TP-LINK-WN722N (BASH 1)

#!/bin/bash

# Basic steps before starting to install driver (run code on sudo su)

sudo apt update && sudo apt upgrade && sudo apt install bc && sudo apt-get install build-essential && sudo apt-get install libelf-dev

# Lets get into 2nd step
# Driver is for 5.10+ kernel (kali)

sudo apt-get install linux-headers-`uname -r` && sudo apt-get install linux-headers-5.10.0-kali6-amd64

# Let start installing basic modules for driver

sudo apt install dkms && sudo rmmod r8188eu.ko

# Lets clone repo and install it

git clone https://github.com/Ethical-Hacking-Tools/rtl8188eus rtl8188eus && cd rtl8188eus

# Blacklist our new driver (or else it will not work)
sudo -i
echo "blacklist r8188eu" > "/etc/modprobe.d/realtek.conf"

#exit

# Reboot PC (commented that line cuz maybe you have to save some files before rebooting) 
#sudo reboot