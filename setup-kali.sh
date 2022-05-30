#!/bin/bash

# Abort if its not running on root
   echo "Checking if you are running this script on su mode or not"
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   sleep 1
   exit
else 
   echo "You are running this script on su mode"
   sleep 1
fi
# Abort if not running on Kali Linux
   echo "Checking if you are running this script on Kali Linux or not"
if [[ ! -e /etc/apt/sources.list.d/kali-linux.list ]]; then
   sleep 1
   echo "You are running this script on KALI LINUX"
   clear
else
   echo "You are not running this script on KALI LINUX"
   exit
fi
# Create a directory for the tools and enter into it
cd .. && mkdir -p Tools && cd Tools
# Update the system
apt update
# Dependencies for kali desktop environment
apt install aptitude
aptitude install libssl-dev bc
apt install build-essential libssl-dev libffi-dev
apt install libssl-dev libffi-dev build-essential
# Dependencies for system fetch
echo "You sure you want to install system fetch? (y/n)"
read -r answer

if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
      echo "Installing system fetch"
      echo -ne '####           (20%)\r'
      sleep 1
      echo -ne '########       (40%)\r'
      sleep 2
      echo -ne '############   (60%)\r'
      sleep 3
      echo -ne '################ (80%)\r'
      sleep 4
      echo -ne '###################(100%)\r'
      echo -ne '\n'
      apt install neofetch;
      echo "installing htop"
      apt install htop;
else
      echo "Skipped installing system fetch"
      sleep 1
fi
# Python3 Dependencies
apt install python3-venv
apt install python3-pip
apt install python3-pip php php-cli
apt install python3-pyqt5 hostapd
python3 -m venv venv
pip install pipenv
# Metasploit Dependencies
apt install zipalign apksigner
apt install openjdk-11-jdk
apt install apktool
# Checking if jarsigniner is working or not
jarsigner
# Unzip the wordlist
gzip -d /usr/share/wordlists/rockyou.txt.gz
# Fix update/upgrade slow issue
git clone https://github.com/Ethical-Hacking-Tools/mirrorscript-v2
cd mirrorscript-v2
python3 mirrorscript-v2.py -h && python3 mirrorscript-v2.py -v -https -src
cd ..
# Clean, update and upgrade your kali-machine
echo "Do you want to clean and upgrade the system now ? (y/n)"
read -r answer

if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Your KALI is now UPDATING.. & UPGRADING.."
        echo -ne '####           (20%)\r'
         sleep 1
         echo -ne '########       (40%)\r'
         sleep 2
         echo -ne '############   (60%)\r'
         sleep 3
         echo -ne '################ (80%)\r'
         sleep 4
         echo -ne '###################(100%)\r'
         echo -ne '\n'
        apt clean; apt update; apt upgrade;
else
        echo "Upgrade later"
        sleep 1
fi
# Lets start cloning tools now
# 1. Phoneinfoga
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash
tar -xvf PhoneInfoga_Linux_x86_64.tar.gz
./phoneinfoga version
mv ./phoneinfoga /usr/bin/phoneinfoga
# 2. Scylla
git clone https://github.com/Ethical-Hacking-Tools/Scylla
cd Scylla
python3 -m pip install -r requirments.txt
cd ..
# 3. Seeker
git clone https://github.com/Ethical-Hacking-Tools/seeker
cd seeker
pip3 install requests
cd ..
# 4. Sherlock
git clone https://github.com/Ethical-Hacking-Tools/sherlock
cd sherlock
pip3 install -r requirements.txt
cd ..
# 5. Osintgram
git clone https://github.com/Ethical-Hacking-Tools/Osintgram
cd Osintgram
pip3 install -r requirements.txt
cd ..
# 6. David-Bombal Scanner and Exploiter
git clone https://github.com/Ethical-Hacking-Tools/red-python-scripts
# 7. Nextfill
git clone https://github.com/thewhiteh4t/nexfil.git
cd nexfil
pip3 install -r requirements.txt
cd ..
# 8. Fluxion
git clone https://github.com/Ethical-Hacking-Tools/fluxion
# 9. Wifipumkin3
git clone https://github.com/Ethical-Hacking-Tools/wifipumpkin3
cd wifipumpkin3
python3 setup.py install
cd ..
# 10. Maryam Scanner (OSINT)
# As it is available on kali-tools repo we can use it from there instead of cloning it.
apt install maryam
# 11. Toutatis
git clone https://github.com/Ethical-Hacking-Tools/toutatis
cd toutatis
python3 setup.py install
cd ..
# 12. XSpear
# Cloning from original repo as it is updated and maintained by maintainers frequently.
git clone https://github.com/hahwul/XSpear
cd XSpear && gem install XSpear && gem install XSpear-1.4.1.gem
cd ..
# 13. SpamWA (Spam WhatsApp)
git clone https://github.com/krypton-byte/SpamWa
# 14. CamPhisher
git clone https://github.com/techchipnet/CamPhish
# 15. MobileSecurityFramework (MSF) (Security Framework Tool for Mobile Devices and Web Applications)
# This tool is just cloned , but we need to install it manually. (cuz of internet connection issues)
git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF
# 16. Privacy Must Be Protected (PIMP)
# TOR Browser is not available on Kali Linux so lets install it manually.
apt install tor torbrowser-launcher
# 17. Matlego (OSINT TOOL)
# As it is available on kali-tools repo we can use it from there instead of cloning it.
apt install maltego
# Worlist for hacking and for other security cracking purpose. (Wordlist)
apt -y install seclists
# 18. DDOS Attack Toolkit (DOS,DDOS)
git clone https://github.com/Ethical-Hacking-Tools/MHDDoS
cd MHDDoS
pip3 install -r requirements.txt
pip install git+https://github.com/MHProDev/PyRoxy.git --upgrade
cd ..
# 19. QRLJacking (QR Hacking Tool)
# Dont clone this tool as of now, because i need to fix this script.
#git clone https://github.com/OWASP/QRLJacking
# 20. BEEF (BeEF) (Browser Exploitation Framework)
# install beef-xss
# I am not gonna install this tool while running the script , because of internet connection issues.
apt install beef-xss
git clone https://github.com/Ethical-Hacking-Tools/beef
# 21. WPSeku (WiFi Security Scanner)
git clone https://github.com/andripwn/WPSeku
cd WPSeku
pip3 install -r requirements.txt
cd ..
## 22. Instabruteforce (Instagram Brute Force Tool)
git clone https://github.com/Ethical-Hacking-Tools/Instabruteforce
cd Instabruteforce
pipenv --python 3.9
pipenv install
cd ..
## Tool cloning ends here
# Lets start downloading/setup kali-env dependencies now.
pwd && ls -l
# Lets download GRUB Theme for Kali Linux
echo "Do you want to download and install custom GRUB theme now ? (y/n)"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   echo -ne '####           (20%)\r'
      sleep 1
      echo -ne '########       (40%)\r'
      sleep 2
      echo -ne '############   (60%)\r'
      sleep 3
      echo -ne '################ (80%)\r'
      sleep 4
      echo -ne '###################(100%)\r'
      echo -ne '\n'
   cd .. && mkdir -p Grub-Theme && cd Grub-Theme
   git clone https://github.com/vandalsoul/dedsec-grub2-theme.git
else
    echo "You can download and install custom GRUB theme later"
    sleep 1
fi
# Lets clean and upgrade the system one more time
echo "Let's do some house keeping on your system ? (y/n)"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Cleaning and upgrading the system now.."
    echo -ne '####           (20%)\r'
      sleep 1
      echo -ne '########       (40%)\r'
      sleep 2
      echo -ne '############   (60%)\r'
      sleep 3
      echo -ne '################ (80%)\r'
      sleep 4
      echo -ne '###################(100%)\r'
      echo -ne '\n'
    sleep 1
   apt clean && apt update && apt upgrade
else
    echo "You can clean and upgrading the system later.."
    sleep 1
fi
# Lets end this here by saying that we are done with Kali-env setup.
echo "Setting up your hacking machine is completed successfully."
echo "Now reboot your Kali Linux and enjoy your hacking experience."
echo "Thanks for using my setup-kali script."
echo "Visit https://github.com/karthik558"
echo "For any queries contact me through email : karthik.lal558@gmail.com"
echo "Happy Hacking.."
sleep 1
exit

# House keeping and script ends here.
##========================================================================================================================##
## KALI DESKTOP ENVIRONMENT SETUP SCRIPT
## AUTHOR: KARTHIK LAL (karthik558)
## DATE:   07.11.2021
## CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX DISTRIBUTION
## TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
## USE AT YOUR OWN RISK.
## LICESNSE: GNU GENERAL PUBLIC LICENSE V3.0
## OPENSOURCE SOFTWARE LICENSE AGREEMENT FOR KALI LINUX DISTRIBUTION 
## https://www.gnu.org/licenses/gpl-3.0.en.html
## HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.
##========================================================================================================================##
### NOTE/WARNING :
### IMPORTANT NOTE : Please do not run this script again , if you have already run this script once.
### This script will take a lot of time to run.
### <=== FONT FIXING FOR KALI LINUX ===>
### For fixing the font issue , download the full font file from this link http://www.mediafire.com/file/on3q6yhfqzo4jh1/Fonts.zip/file
### And extract it in /usr/local/share/fonts or /usr/share/fonts folder.
### <=== FIX GRUB RESOLUTION AND THEME FIX AFTER INSTALLING CUSTOM THEME OR FOR CHANGING THE RESOLTION OF DEFAULT KALI GRUB ===>
### /etc/default/grub.d folder is used to change the resolution of default Kali GRUB.
### For changing the resolution of default Kali GRUB , you can use this command : sudo nano /etc/default/grub.d/20-custom.cfg
### Change the resolution of default Kali GRUB to your liking.
### Run this command : sudo update-grub && sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot.
### <=== Fix permission issue after running this script. ===>
### chown -R username: /home/username (username is your username) eg: chown -R root: /home/root (This will change the permission of /home/root folder to root user)
### <=== Change ZSH shell to bash shell after running this script. ===>
### chsh -s /bin/bash (This will change the default shell to bash)
### THANKS FOR USING THIS SCRIPT.
### WE ARE HAPPY TO HAVE YOU ON OUR TEAM.
### WE ARE ALWAYS HERE TO HELP YOU (JUST RAISE A ISSUE ON GITHUB IF YOU HAVE ISSUE WITH THIS SCRIPT).
### CODED BY : KARTHIK LAL
### WEBSITE : https://karthik558.tk
### EMAIL : karthik.lal558@gmail.com
### GITHUB : karthik558
### CONTRIBUTIONS ARE WELCOME. :)