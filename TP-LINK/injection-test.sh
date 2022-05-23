# Default interface set to 0 // change this accoding to you pc
# LICENSE: GPL-3.0-or-later
# Author: KARTHIK LAL
# Copyright (C) 2022 KARTHIK LAL
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Injection test is done on interface 0/1

#!/bin/bash

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
echo "Select the correct interface to test packet-injection ! (0/1)"
read -r answer
if [[ $answer == 0 ]]; then
   echo "Injecting packets on interface 0"
   ifconfig wlan0 down;
   iwconfig wlan0 mode monitor;
   ifconfig wlan0 up;
   iwconfig wlan0;
   echo "Injecting packets on interface 0"
   aireplay-ng --test wlan0
   echo "Packet injection test done on interface 0 and its working fine"
else 
   echo "Injecting packets on interface 1"
   ifconfig wlan1 down;
   iwconfig wlan1 mode monitor;
   ifconfig wlan1 up;
   iwconfig wlan1;
   echo "Injecting packets on interface 1"
   aireplay-ng --test wlan1
   echo "Packet injection test done on interface 1 and its working fine"
fi