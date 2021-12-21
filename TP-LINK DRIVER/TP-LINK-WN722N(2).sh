# Wifi Adapter Driver for Linux 
# TP-LINK-WN722N (BASH 2)

#!/bin/bash

# Welcome back again , lets get into final step
# As always run script on (su)

sudo apt update && cd r8188eus && sudo make && sudo make install && sudo modprobe 8188eu