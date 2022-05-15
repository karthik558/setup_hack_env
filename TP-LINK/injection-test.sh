# Default interface set to 0 // change this accoding to you pc
# LICENSE: GPL-3.0-or-later
# Author: KARTHIK LAL
# Copyright (C) 2022 KARTHIK LAL
# Let's start the tool
# Default interface set to 0 // change this accoding to you pc
# Injection test is done on interface 0
#!/bin/bash
# Path: TP-LINK DRIVER\injection-test.sh

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

# Lets start the injection test
echo "Injection test is starting on interface 0 (default)"
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
iwconfig wlan0
sudo aireplay-ng --test wlan0
echo "Packet Injection test is running on interface 0 and its working fine"