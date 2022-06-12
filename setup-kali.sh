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
apt install apktool #https://ibotpeaches.github.io/Apktool/install/ (Download wrapper script and apktool.jar file and move it to /bin, this is latest stable apktool version)
# Checking if jarsigniner is working or not
jarsigner
# Unzip the default kali wordlist and remote the tar.gz file
gzip -d /usr/share/wordlists/rockyou.txt.gz
# Fix update/upgrade slow issue on Kali Linux (Kali Mirrorscript-v2 by IceM4nn automatically select the best kali mirror server and apply the configuration)
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
# 1. Phoneinfoga (Information gathering & OSINT framework for phone numbers)
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash
tar -xvf PhoneInfoga_Linux_x86_64.tar.gz
./phoneinfoga version
mv ./phoneinfoga /usr/bin/phoneinfoga
# 2. Scylla (The Simplistic Information Gathering Engine | Find Advanced Information on a Username, Website, Phone Number, etc.)
git clone https://github.com/Ethical-Hacking-Tools/Scylla
cd Scylla
python3 -m pip install -r requirments.txt
cd ..
# 3. Seeker (Accurately Locate Smartphones using Social Engineering)
git clone https://github.com/Ethical-Hacking-Tools/seeker
cd seeker
pip3 install requests
cd ..
# 4. Sherlock (Hunt down social media accounts by username across social networks)
git clone https://github.com/Ethical-Hacking-Tools/sherlock
cd sherlock
pip3 install -r requirements.txt
cd ..
# 5. Osintgram (Osintgram is a OSINT tool on Instagram. It offers an interactive shell to perform analysis on Instagram account of any users by its nickname)
git clone https://github.com/Ethical-Hacking-Tools/Osintgram
cd Osintgram
pip3 install -r requirements.txt
cd ..
# 6. David-Bombal Scanner and Exploiter (David-Bombal script is very useful for performing various types of attacks on a target machine)
git clone https://github.com/Ethical-Hacking-Tools/red-python-scripts
# 7. Nextfill (OSINT tool for finding profiles by username)
git clone https://github.com/thewhiteh4t/nexfil.git
cd nexfil
pip3 install -r requirements.txt
cd ..
# 8. Fluxion (Fluxion is a remake of linset by vk496 with enhanced functionality.)
git clone https://github.com/Ethical-Hacking-Tools/fluxion
# 9. Wifipumkin3 (Powerful framework for rogue access point attack.)
git clone https://github.com/Ethical-Hacking-Tools/wifipumpkin3
cd wifipumpkin3
python3 setup.py install
cd ..
# 10. Maryam Scanner (OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering.)
# As it is available on kali-tools repo we can use it from there instead of cloning it.
apt install maryam
# 11. Toutatis (Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more.)
git clone https://github.com/Ethical-Hacking-Tools/toutatis
cd toutatis
python3 setup.py install
cd ..
# 12. XSpear (Powerfull XSS Scanning and Parameter analysis tool&gem)
# Cloning from original repo as it is updated and maintained by maintainers frequently.
git clone https://github.com/hahwul/XSpear
cd XSpear && gem install XSpear && gem install XSpear-1.4.1.gem
cd ..
# 13. SpamWA (A simple python script that can be used to send SMS messages to a list of numbers)
git clone https://github.com/krypton-byte/SpamWa
# 14. CamPhisher (Grab cam shots from target's phone front camera or PC webcam just sending a link.)
git clone https://github.com/techchipnet/CamPhish
# 15. Mobile Security Framework (Mobile Security Framework (MobSF) is an automated, all-in-one mobile application (Android/iOS/Windows) pen-testing, malware analysis and security assessment framework capable of performing static and dynamic analysis.)
# This tool is just cloned , but we need to install it manually. (cuz of internet connection issues)
git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF
# 16. Privacy Must Be Protected (PIMP)
# TOR Browser is not available on Kali Linux by default so lets install it manually.
apt install tor torbrowser-launcher #(https://www.torproject.org/download/download.html.en)
# 17. Matlego (OSINT TOOL) (Maltego is a program that can be used to determine the relationships and real world links between: People. Groups of people (social networks) Companies.)
# As it is available on kali-tools repo we can use it from there instead of cloning it.
apt install maltego
# SecList (SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more.)
apt -y install seclists
# 18. MHDDOS (Best DDoS Attack Script Python3, Cyber Attack With 36 Methods)
git clone https://github.com/Ethical-Hacking-Tools/MHDDoS
cd MHDDoS
pip3 install -r requirements.txt
pip install git+https://github.com/MHProDev/PyRoxy.git --upgrade
cd ..
# 19. QRLJacking (QRLJacking or Quick Response Code Login Jacking is a simple-but-nasty attack vector affecting all the applications that relays on “Login with QR code” feature as a secure way to login into accounts which aims for hijacking users session by attackers.)
# Dont clone this tool as of now, because i need to fix this script.
#git clone https://github.com/OWASP/QRLJacking
# 20. BEEF (Browser Exploitation Framework) (BeEF is short for The Browser Exploitation Framework. It is a penetration testing tool that focuses on the web browser. It is a framework that allows you to create a custom user-agent and inject malicious code into the browser.)
# install beef-xss
apt install beef-xss
git clone https://github.com/Ethical-Hacking-Tools/beef
# 21. WPSeku (WPSeku is a black box WordPress vulnerability scanner that can be used to scan remote WordPress installations to find security issues.)
git clone https://github.com/andripwn/WPSeku
cd WPSeku
pip3 install -r requirements.txt
cd ..
## 22. Instabruteforce (Hacking-tool termux-tools termux noob-friendly instagram-bot bruteforce-password-cracker wordlist-techniques).
git clone https://github.com/Ethical-Hacking-Tools/Instabruteforce
cd Instabruteforce
pipenv --python 3.9
pipenv install
cd ..
# 23. UserFinder (OSINT tool for finding profiles by username.)
git clone https://github.com/Ethical-Hacking-Tools/UserFinder
## 24. SHARK (A shark is a tool that will help you do Phishing in an advanced way so no one checks and identify that you are doing phishing.For those guys who Don't know about Phishing let me explain "Phishing is the fraudulent attempt to obtain sensitive information or data, such as usernames, passwords, by disguising oneself as a trustworthy entity in an electronic communication. Typically carried out by email spoofing, instant messaging, and text messaging, phishing often directs users to enter personal information at a fake website which matches the look and feel of the legitimate site. as shown in MR ROBOT.)
sudo wget -qO- https://github.com/Bhaviktutorials/shark/raw/master/setup | sudo bash
## 25. MITM Attack
# MITM Attack is a tool that can be used to perform MITM attacks on the network.
git clone https://github.com/karthik558/CREATE-MITM-AP
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