# Default interface set to 0 // change this accoding to you pc

#!/bin/bash

sudo ifconfig wlan0 down && sudo airmon-ng check kill && sudo iwconfig wlan0 mode monitor && sudo ifconfig wlan0 up && iwconfig && sudo aireplay-ng --test wlan0