# Kali Desktop Environment Setup 

#!/bin/bash

pwd

mkdir Tools && mkdir Themes

cd Tools

# Dependencies 

sudo apt-get install aptitude && sudo aptitude install libssl-dev bc

sudo apt-get install neofetch build-essential libssl-dev libffi-dev python-dev

sudo apt-get install python3-venv

sudo apt install python3-pip

# Fix Kali update && upgrade slow issue

git clone https://github.com/Ethical-Hacking-Tools/mirrorscript-v2

cd mirrorscript-v2

python3 mirrorscript-v2.py -h && python3 mirrorscript-v2.py -v -https -src

cd ..

sudo apt clean && sudo apt update & sudo apt upgrade

# Phoneinfoga

curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash

tar -xvf PhoneInfoga_Linux_x86_64.tar.gz

./phoneinfoga version

sudo mv ./phoneinfoga /usr/bin/phoneinfoga

# Scylla

git clone https://github.com/Ethical-Hacking-Tools/Scylla

cd Scylla

sudo python3 -m pip install -r requirments.txt

cd ..

# Seeker 

git clone https://github.com/Ethical-Hacking-Tools/seeker

cd seeker

sudo apt update && sudo apt install python3-pip php

pip3 install requests

cd ..

# Storm-Breaker

git clone https://github.com/Ethical-Hacking-Tools/Storm-Breaker

cd Storm-Breaker

sudo bash linux-installer.sh

sudo python3 -m pip install -r requirments.txt

# sudo python3 Storm-Breaker.py

cd ..

# Sherlock

git clone https://github.com/Ethical-Hacking-Tools/sherlock sherlock

cd sherlock

sudo python3 -m pip install -r requirements.txt

# python3 sherlock --help

cd ..

# Osintgram

git clone https://github.com/Ethical-Hacking-Tools/Osintgram

cd Osintgram

sudo python3 -m venv venv

pip install -r requirements.txt

cd ..

# David-Bombal Script's 

git clone https://github.com/Ethical-Hacking-Tools/red-python-scripts

# NextFill

git clone https://github.com/thewhiteh4t/nexfil.git

cd nexfil

pip3 install -r requirements.txt

python3 nexfil.py -h

cd ..

# Facebook Brute Force

git clone https://github.com/Ethical-Hacking-Tools/BluForce-FB BluForce

cd BluForce

pip3 install mechanize

cd ..

# Fluxion

git clone https://github.com/Ethical-Hacking-Tools/fluxion Fluxion

cd Fluxion

#sudo ./fluxion.sh -i

cd ..

# Wifipumkin3

sudo apt install libssl-dev libffi-dev build-essential

git clone https://github.com/Ethical-Hacking-Tools/wifipumpkin3 wifipumpkin3

cd wifipumpkin3

sudo apt-get install python3-pyqt5 hostapd

sudo python3 setup.py install

cd ..

# MARYAM (OSINT TOOL)

sudo apt-get install maryam

# Cam-Hacker

git clone https://github.com/Ethical-Hacking-Tools/Cam-Hackers

cd Cam-Hacker

pip3 install requests

pip3 install colorama

cd ..

# Toutatis

git clone https://github.com/Ethical-Hacking-Tools/toutatis

cd toutatis

python3 setup.py install

cd ..

# MHDDos

git clone https://github.com/Ethical-Hacking-Tools/MHDDoS

cd MHDDoS

pip3 install -r requirements.txt

pip install git+https://github.com/MHProDev/PyRoxy.git --upgrade

cd ..

# QRLJacking Attack

git clone https://github.com/OWASP/QRLJacking

## Install this for QRLJacking Attack https://github.com/mozilla/geckodriver/releases (download latest) and run this command https://github.com/OWASP/QRLJacking/tree/master/QRLJacker

cd QRLJacking/QRLJacker

pip install -r requirements.txt

python3 QrlJacker.py --help

cd ../../../

## GRUB THEME ##

cd Themes 

git clone https://github.com/vandalsoul/dedsec-grub2-theme.git

cd dedsec-grub2-theme

# sudo python3 install.py

cd ../../

####
####
####
####
####
#### Some NOTES/INSTRUCTIONS
####
#### Download Full Font : http://www.mediafire.com/file/on3q6yhfqzo4jh1/Fonts.zip/file
####
#### /etc/default/grub.d (Grub resolution and theme fix) (after updating grub :- sudo update-grub)
####
#### Fix some permission issue
#### sudo chown -R username: /home/username (eg: sudo chown -R kali: /home/kali) (This will fix permission issue on home directory after doing ./clone)
#### chsh -s /bin/bash (this is to change zsh to bash) 
#### 
####
####
####
