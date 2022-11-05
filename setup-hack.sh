#!/bin/bash

# Select the color of the text in the terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
VIOLET='\033[0;35m'
CYAN='\033[0;36m'
BLACK='\033[0;30m'
NC='\033[0m' # No Color

#        :::    :::     :::      ::::::::  :::    :::              :::::::::: ::::    ::: :::     ::: 
#      :+:    :+:   :+: :+:   :+:    :+: :+:   :+:               :+:        :+:+:   :+: :+:     :+:  
#     +:+    +:+  +:+   +:+  +:+        +:+  +:+                +:+        :+:+:+  +:+ +:+     +:+   
#    +#++:++#++ +#++:++#++: +#+        +#++:++   +#++:++#++:++ +#++:++#   +#+ +:+ +#+ +#+     +:+    
#   +#+    +#+ +#+     +#+ +#+        +#+  +#+                +#+        +#+  +#+#+#  +#+   +#+      
#  #+#    #+# #+#     #+# #+#    #+# #+#   #+#               #+#        #+#   #+#+#   #+#+#+#        
# ###    ### ###     ###  ########  ###    ###              ########## ###    ####     ###           

# Abort if its not running on root
echo "Checking if you are running this script on su mode or not"
if [[ $EUID -ne 0 ]]; then
   printf "${RED}This script must be run as root${NC}\n"
   sleep 1
   exit
else
   printf "${GREEN}You are running this script on su mode${NC}\n"
   sleep 1
   clear
fi
# Abort if not running on Kali Linux or ParrotOS
echo "Checking if you are running this script on Kali Linux or ParrotOS"
if [[ -f /etc/os-release ]]; then
   . /etc/os-release
   OS=$NAME
   VER=$VERSION_ID
   if [[ $OS == "Kali GNU/Linux" ]]; then
      printf "${GREEN}You are running this script on Kali Linux${NC}\n"
      sleep 1
      clear
   elif [[ $OS == "Parrot GNU/Linux" ]]; then
      printf "${GREEN}You are running this script on Parrot OS${NC}\n"
      sleep 1
      clear
   else
      printf "${RED}You are not running this script on Kali Linux or Parrot OS${NC}\n"
      sleep 1
      exit
   fi

# Pulling the latest changes from the repository
printf "${BLUE}Fetching the repository and pulling the latest changes from the repository${NC}\n"
git fetch https://github.com/karthik558/setup_hack_env.git && git pull https://github.com/karthik558/setup_hack_env.git
sleep 1
clear

# Create a directory for the tools and enter into it
printf "${BLUE}Creating a directory for clonning the tools and entering into it${NC}\n"
cd .. && mkdir -p Tools && cd Tools
clear

# Update the system
apt update

# Dependencies for KaliLinux and ParrotOS desktop environment
apt install terminator
apt install aptitude
aptitude install libssl-dev bc
apt install build-essential libssl-dev libffi-dev
apt install libssl-dev libffi-dev build-essential
apt install tar tor curl python3 python3-scapy network-manager

# Dependencies for system fetch
printf "${BLUE}You sure you want to install SYSTEM_FETCH and HTOP? (y/n)${NC}\n"
read -r answer

if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${GREEN}Installing system fetch${NC}\n"
   echo -ne '**          (20%)\r'
   sleep 1
   echo -ne '****        (40%)\r'
   sleep 2
   echo -ne '******      (60%)\r'
   sleep 3
   echo -ne '********      (80%)\r'
   sleep 4
   echo -ne '**********   (100%)\r'
   echo -ne '\n'
   apt install neofetch
   printf "${BLUE}Installing HTOP${NC}\n"
   apt install htop
   clear
else
   printf "${RED}Skipped installing SYSTEM_FETCH and HTOP${NC}\n"
   sleep 1
   clear
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
# Unzip the default wordlist and remove the tar.gz file
gzip -d /usr/share/wordlists/rockyou.txt.gz

## Clone the tools from the repository starts here
# Fix update/upgrade slow issue on Kali Linux (Kali Mirrorscript-v2 by IceM4nn automatically select the best kali mirror server and apply the configuration)
printf "${BLUE}You sure you want to install Kali Mirrorscript-v2 by IceM4nn? (y/n)${NC}\n"
read -r answer

if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${GREEN}Installing Kali Mirrorscript-v2 by IceM4nn${NC}\n"
   echo -ne '****        (40%)\r'
   sleep 1
   echo -ne '********      (80%)\r'
   sleep 2
   echo -ne '**********   (100%)\r'
   echo -ne '\n'
   git clone https://github.com/Ethical-Hacking-Tools/mirrorscript-v2
   cd mirrorscript-v2
   git pull https://github.com/IceM4nn/mirrorscript-v2
   python3 mirrorscript-v2.py -h && python3 mirrorscript-v2.py -v -https -src
   cd ..
else 
   printf "${RED}Skipped installing Kali Mirrorscript-v2 by IceM4nn${NC}\n"
   sleep 1
   clear
fi

# Clean, update and upgrade your hacking-machine now
printf "${BLUE}Do you want to clean and upgrade the system now ? (y/n)${NC}\n"
read -r answer

if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${YELLOW}Your HACKING-MACHINE is now UPDATING.. && UPGRADING..${NC}\n"
   echo -ne '**          (20%)\r'
   sleep 1
   echo -ne '****        (40%)\r'
   sleep 2
   echo -ne '******      (60%)\r'
   sleep 3
   echo -ne '********      (80%)\r'
   sleep 4
   echo -ne '**********   (100%)\r'
   echo -ne '\n'
   apt clean
   apt update
   apt upgrade
   clear
else
   printf "${GREEN}UPGRADE LATER${NC}\n"
   sleep 1
   clear
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
git pull https://github.com/MandConsultingGroup/Scylla
python3 -m pip install -r requirments.txt
cd ..
# 3. Seeker (Accurately Locate Smartphones using Social Engineering)
git clone https://github.com/Ethical-Hacking-Tools/seeker
cd seeker
git pull https://github.com/thewhiteh4t/seeker
pip3 install requests
cd ..
# 4. Sherlock (Hunt down social media accounts by username across social networks)
git clone https://github.com/Ethical-Hacking-Tools/sherlock
cd sherlock
git pull https://github.com/sherlock-project/sherlock
pip3 install -r requirements.txt
cd ..
# 5. Osintgram (Osintgram is a OSINT tool on Instagram. It offers an interactive shell to perform analysis on Instagram account of any users by its nickname)
git clone https://github.com/Ethical-Hacking-Tools/Osintgram
cd Osintgram
git pull https://github.com/Datalux/Osintgram
pip3 install -r requirements.txt
cd ..
# 6. David-Bombal Scanner and Exploiter (David-Bombal script is very useful for performing various types of attacks on a target machine)
git clone https://github.com/Ethical-Hacking-Tools/red-python-scripts
cd red-python-scripts
git pull https://github.com/davidbombal/red-python-scripts
cd ..
# 7. Nextfill (OSINT tool for finding profiles by username)
git clone https://github.com/thewhiteh4t/nexfil.git
cd nexfil
git pull https://github.com/thewhiteh4t/nexfil
pip3 install -r requirements.txt
cd ..
# 8. Fluxion (Fluxion is a remake of linset by vk496 with enhanced functionality.)
git clone https://github.com/Ethical-Hacking-Tools/fluxion
cd fluxion
git pull https://github.com/FluxionNetwork/fluxion
cd ..
# 9. Wifipumkin3 (Powerful framework for rogue access point attack.)
git clone https://github.com/Ethical-Hacking-Tools/wifipumpkin3
cd wifipumpkin3
git pull https://github.com/P0cL4bs/wifipumpkin3
python3 setup.py install
cd ..
# 10. Maryam Scanner (OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering.)
# As it is available on debian-repository we can install it using apt-install
apt install maryam
# 11. Toutatis (Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more.)
git clone https://github.com/Ethical-Hacking-Tools/toutatis
cd toutatis
git pull https://github.com/megadose/toutatis
python3 setup.py install
cd ..
# 12. XSpear (Powerfull XSS Scanning and Parameter analysis tool&gem)
# Cloning from original repo as it is updated and maintained by maintainers frequently.
git clone https://github.com/hahwul/XSpear
cd XSpear && gem install XSpear && gem install XSpear-1.4.1.gem
cd ..
# 13. SpamWA (A simple python script that can be used to send SMS messages to a list of numbers)
git clone https://github.com/krypton-byte/SpamWa
cd SpamWa
git pull https://github.com/krypton-byte/SpamWa
cd ..
# 14. CamPhisher (Grab cam shots from target's phone front camera or PC webcam just sending a link.)
git clone https://github.com/techchipnet/CamPhish
# 15. Mobile Security Framework (Mobile Security Framework (MobSF) is an automated, all-in-one mobile application (Android/iOS/Windows) pen-testing, malware analysis and security assessment framework capable of performing static and dynamic analysis.)
# This tool is just cloned , but we need to install it manually. (cuz of internet connection issues)
git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF
cd Mobile-Security-Framework-MobSF
sudo ./setup.sh
cd ..
# 16. Privacy Must Be Protected (PIMP)
# TOR Browser is not available on Kali Linux by default so lets install it manually.
apt install tor torbrowser-launcher #(https://www.torproject.org/download/download.html.en) #Skips on ParrotOS
# 17. Matlego (OSINT TOOL) (Maltego is a program that can be used to determine the relationships and real world links between: People. Groups of people (social networks) Companies.)
# As it is available on debian repository we can install it using apt-install
apt install maltego #Skips on ParrotOS
# SecList (SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more.)
apt -y install seclists
# 18. MHDDOS (Best DDoS Attack Script Python3, Cyber Attack With 36 Methods)
git clone https://github.com/MatrixTM/MHDDoS
cd MHDDoS
pip3 install -r requirements.txt
pip install git+https://github.com/MHProDev/PyRoxy.git --upgrade
cd ..
# 19. QRLJacking (QRLJacking or Quick Response Code Login Jacking is a simple-but-nasty attack vector affecting all the applications that relays on “Login with QR code” feature as a secure way to login into accounts which aims for hijacking users session by attackers.)
# Dont clone this tool as of now, because i need to fix this script.
#git clone https://github.com/OWASP/QRLJacking
# 20. BEEF (Browser Exploitation Framework) (BeEF is short for The Browser Exploitation Framework. It is a penetration testing tool that focuses on the web browser. It is a framework that allows you to create a custom user-agent and inject malicious code into the browser.)
# install beef-xss
#apt install beef-xss
#git clone https://github.com/beefproject/beef
# 21. WPSeku (WPSeku is a black box WordPress vulnerability scanner that can be used to scan remote WordPress installations to find security issues.)
git clone https://github.com/andripwn/WPSeku
cd WPSeku
pip3 install -r requirements.txt
cd ..
## 22. Instabruteforce (Hacking-tool termux-tools termux noob-friendly instagram-bot bruteforce-password-cracker wordlist-techniques).
git clone https://github.com/Ethical-Hacking-Tools/Instabruteforce
cd Instabruteforce
git pull https://github.com/Hackertrackersj/Instabruteforce
pipenv --python 3.9
pipenv install
cd ..
# 23. UserFinder (OSINT tool for finding profiles by username.)
git clone https://github.com/Ethical-Hacking-Tools/UserFinder
cd UserFinder
git pull https://github.com/mishakorzik/UserFinder
cd ..
## 24. SHARK (A shark is a tool that will help you do Phishing in an advanced way so no one checks and identify that you are doing phishing.For those guys who Don't know about Phishing let me explain "Phishing is the fraudulent attempt to obtain sensitive information or data, such as usernames, passwords, by disguising oneself as a trustworthy entity in an electronic communication. Typically carried out by email spoofing, instant messaging, and text messaging, phishing often directs users to enter personal information at a fake website which matches the look and feel of the legitimate site. as shown in MR ROBOT.)
sudo wget -qO- https://github.com/Bhaviktutorials/shark/raw/master/setup | sudo bash
## 25. MITM Attack
# MITM Attack is a tool that can be used to perform MITM attacks on the network.
git clone https://github.com/karthik558/CREATE-MITM-AP
sudo apt install mdk3
## 26. Netdiscover (Netdiscover is an active/passive address reconnaissance tool, mainly developed for those wireless networks without dhcp server, when you are wardriving. It can be also used on hub/switched networks.)
sudo apt install netdiscover #skips on ParrotOS
## 27. whoami-project
git clone https://github.com/owerdogan/whoami-project #skips on ParrotOS
cd whoami-project
git pull https://github.com/owerdogan/whoami-project
sudo make install
cd ..
## 28. Any-Apk
git clone https://github.com/kinghacker0/Any-Apk
## 29. UPI-INT
git clone https://github.com/Ethical-Hacking-Tools/UPI-INT
cd UPI-INT
git pull https://github.com/BiswajeetRay7/UPI-INT
sudo apt-get install nodejs
npm install
cd ..
## 30. Track-IP
git clone https://github.com/Ethical-Hacking-Tools/track-ip
cd track-ip
git pull https://github.com/htr-tech/track-ip
cd ..
## 31. Trape (People tracker on the Internet: OSINT analysis and research tool by Jose Pino)
git clone https://github.com/Ethical-Hacking-Tools/trape
cd trape
git pull https://github.com/jofpin/trape
pip3 install -r requirements.txt
## Tool cloning ends here

# Lets start downloading/setup hack-env dependencies now.
pwd && ls -l

# Lets download GRUB Theme for Kali Linux [WIll not work for Parrot BTW]
printf "${RED}Do you want to download and install custom GRUB theme now ? (y/n)${NC}\n"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   echo -ne '**          (20%)\r'
   sleep 1
   echo -ne '****        (40%)\r'
   sleep 2
   echo -ne '******      (60%)\r'
   sleep 3
   echo -ne '********      (80%)\r'
   sleep 4
   echo -ne '**********   (100%)\r'
   echo -ne '\n'
   clear && cd .. && mkdir -p Grub-Theme && cd Grub-Theme
   git clone https://github.com/vandalsoul/dedsec-grub2-theme.git
else
   printf "${RED}You can download and install custom GRUB theme later by running this script again.${NC}\n"
   sleep 1
   clear
fi

# Lets clean and upgrade the system one more time
printf "${YELLOW}Let's do some house keeping on your system ? (y/n) ${NC}\n"
read -r answer
if [[ $answer =~ ^([yY][eE][sS]|[yY])$ ]]; then
   printf "${RED}Cleaning and upgrading your system now.. ${NC}\n"
   echo -ne '**          (20%)\r'
   sleep 1
   echo -ne '****        (40%)\r'
   sleep 2
   echo -ne '******      (60%)\r'
   sleep 3
   echo -ne '********      (80%)\r'
   sleep 4
   echo -ne '**********   (100%)\r'
   echo -ne '\n'
   sleep 1
   clear && apt clean && apt update && apt upgrade && apt autoremove && apt dist-upgrade
else
   printf "${YELLOW}You can clean and upgrade your system later.. ${NC}\n"
   sleep 1
   clear
fi

# Lets end this here by saying that we are done with HACKING setup.
printf "${GREEN}SETTING UP YOUR HACKING MACHINE IS COMPLETED. ${NC}\n"
sleep 2
printf "${GREEN}NOW REBOOT YOUR DEVICE AND START HACKING.... ${NC}\n"
sleep 2
clear
printf "${CYAN}THANK YOU FOR USING MY SETUP-HACKING-SCRIPT. ${NC}\n"
sleep 2
clear
printf "${CYAN}PLEASE VISIT https://github.com/karthik558 AND STAR MY PROJECTS IF YOU LIKE... ${NC}\n"
sleep 2
printf "${CYAN}FOR ANY QUERY'S CONTACT ME THROUGH email:karthiklal@duck.com ${NC}\n"

# '##::::'##::::'###::::'########::'########::'##:::'##::::'##::::'##::::'###:::::'######::'##:::'##:'####:'##::: ##::'######:::
#  ##:::: ##:::'## ##::: ##.... ##: ##.... ##:. ##:'##::::: ##:::: ##:::'## ##:::'##... ##: ##::'##::. ##:: ###:: ##:'##... ##::
#  ##:::: ##::'##:. ##:: ##:::: ##: ##:::: ##::. ####:::::: ##:::: ##::'##:. ##:: ##:::..:: ##:'##:::: ##:: ####: ##: ##:::..:::
#  #########:'##:::. ##: ########:: ########::::. ##::::::: #########:'##:::. ##: ##::::::: #####::::: ##:: ## ## ##: ##::'####:
#  ##.... ##: #########: ##.....::: ##.....:::::: ##::::::: ##.... ##: #########: ##::::::: ##. ##:::: ##:: ##. ####: ##::: ##::
#  ##:::: ##: ##.... ##: ##:::::::: ##::::::::::: ##::::::: ##:::: ##: ##.... ##: ##::: ##: ##:. ##::: ##:: ##:. ###: ##::: ##::
#  ##:::: ##: ##:::: ##: ##:::::::: ##::::::::::: ##::::::: ##:::: ##: ##:::: ##:. ######:: ##::. ##:'####: ##::. ##:. ######:::
# ..:::::..::..:::::..::..:::::::::..::::::::::::..::::::::..:::::..::..:::::..:::......:::..::::..::....::..::::..:::......::::

# Print final message/greetings to the $USER
clear
printf "${GREEN}HAPPY HACKING PEOPLES.....${NC}\n"
sleep 2

# Information about the bugs/issues after using this script
printf "${YELLOW} PLEASE READ THE BRIEF ABOUT THIS SCRIPT UNDER (setup-hack.sh)${NC}\n"
printf "${YELLOW} IF YOU FIND ANY BUGS OR ISSUES PLEASE REPORT TO ME THROUGH EMAIL : karthiklal@duck.com ${NC}\n"
sleep 2
clear

# Print Good Morning/Afternoon/Evening/Night message depending on the time of the day
if [[ $(date +%H) -ge 0 && $(date +%H) -lt 12 ]]; then
   printf "${BLUE}Good Morning, Have a Nice Day :) ${NC}\n"
elif [[ $(date +%H) -ge 12 && $(date +%H) -lt 16 ]]; then
   printf "${BLUE}Good Afternoon, Had your lunch? :-* ${NC}\n"
elif [[ $(date +%H) -ge 16 && $(date +%H) -lt 20 ]]; then
   printf "${BLUE}Good Evening, Had tea?  ;-) ${NC}\n"
else
   printf "${BLUE}Good Night, Sweet Dreams :-) ${NC}\n"
fi
sleep 2

# Wait for user input before closing the terminal
printf "${RED}Press any key to exit the terminal...${NC}\n"
read -r -n 1 -s
exit 0
# SCRIPT ENDS HERE

## Brief about this script >>.
## Author/Developer Information >>.
## License Information >>.
##
# ├── HACKING DESKTOP ENVIRONMENT SETUP SCRIPT
# ├── AUTHOR: KARTHIK LAL (https://github.com/karthik558) (https://karthiklal.live)
# ├── DATE:   07.11.2021
# ├── CYBERSECURITY AND HACKING TOOLS FOR KALI LINUX AND PARROT SECURITY-OS DISTRIBUTION
# ├── TOOLS ARE PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND AND THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE CAUSED BY THE USE OF THESE TOOLS.
# ├── USE AT YOUR OWN RISK.
# └── HACKING IS ILLEGAL. DO NOT ATTEMPT TO HACK. THIS IS A TOOL FOR EDUCATIONAL PURPOSE ONLY.

## Basic script usage issues >>.
## Bugs and issues after running this script >>.
## How to fix them >>.
##
# ├── IMPORTANT NOTE : Please do not run this script again , if you have already run this script once.
# ├── This script will take a lot of time to run.
# ├── <=== FONT FIXING FOR KALI LINUX AND PARROTOS ===>
# ├── For fixing the font issue , download the full font file from this link http://www.mediafire.com/file/on3q6yhfqzo4jh1/Fonts.zip/file
# ├── And extract it in /usr/local/share/fonts or /usr/share/fonts folder.
# ├── <=== FIX GRUB RESOLUTION AND THEME FIX AFTER INSTALLING CUSTOM THEME OR FOR CHANGING THE RESOLTION OF DEFAULT KALI GRUB ===>
# ├── New bug on kali-linux (windows partition is not showing on grub after updating and upgrading system) -> FIX GRUB_DISABLE_OS_PROBER=false add on /etc/default/grub
# ├── /etc/default/grub.d folder is used to change the resolution of default Kali GRUB.
# ├── For changing the resolution of default Kali GRUB , you can use this command : sudo nano /etc/default/grub.d/20-custom.cfg
# ├── Change the resolution of default Kali GRUB to your liking.
# ├── Run this command : sudo update-grub && sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot.
# ├── <=== Fix permission issue after running this script. ===>
# ├── chown -R username: /home/username (username is your username) eg: chown -R root: /home/root (This will change the permission of /home/root folder to root user)
# ├── In case you get any error while logging in to your kali linux desktop environment , you can use this command to fix the issue : sudo dpkg --configure -a (ctrl + alt + f1/f2) and then login to your kali linux -> sudo apt-get update && sudo apt-ger upgrade -> and type the command sudo dpkg --configure -a and press enter. This will fix the issue. Then Restart your kali linux.
# ├── sudo chown -R kali home/kali (This will change the permission of /home/kali folder to kali user) (kali is your username)
# ├── <=== Change ZSH shell to bash shell after running this script. ===>
# └── chsh -s /bin/bash (This will change the default shell to bash)

## Configure Proxychains for using proxychains with both kali-linux and parrotos >>.
##
# ├── For configuring the proxychains, Do the following steps:
# ├── 1. Open the file sudo nano /etc/proxychains4.conf in a text editor.
# ├── 2. Comment the line strict_chain and Uncomment the line dynamic_chain.
# ├── 3. Add the socks proxy to the file to the end of the file. [socks5  127.0.0.1 9050]
# ├── 4. Save the file and exit.
# ├── 5. service tor start && service tor status
# └── 6. proxychains wwww.duckduckgo.com (for testing if the proxychains is working or not)

## Declaration for using my script >>.
##
# ├── THANKS FOR USING THIS SCRIPT.
# ├── WE ARE HAPPY TO HAVE YOU ON OUR TEAM.
# ├── WE ARE ALWAYS HERE TO HELP YOU (JUST RAISE A ISSUE ON GITHUB IF YOU HAVE ISSUE WITH THIS SCRIPT).
# ├── THIS CODE IS WRITTEN BY : KARTHIK LAL (karthiklal@duck.com/karthiklal.live)
# ├── WEBSITE : https://karthiklal.live
# ├── EMAIL : karthik.lal558@gmail.com/karthiklal@duck.com
# ├── GITHUB : karthik558
# └── CONTRIBUTIONS ARE WELCOME. :)
