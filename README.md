# Setup Hack Environment (Kali/ParrotOS) 

This is a diverse collection of scripts used for OSINT, ethical hacking, and web application security testing. The scripts cover a range of tasks, from automating daily tasks to driver installation, and are suitable for use on Kali-Linux and ParrotOS. The set of tools includes TP-LINK-722N wifi drivers, which can be accessed through the provided instructions, and is cloned from the Ethical-Hacking-Tools repository. Contributions and suggestions are always welcome, and bug reports should be directed to the author, with a signature for identification.

![](https://img.shields.io/github/license/karthik558/setup_hack_env?style=for-the-badge)
![](https://img.shields.io/github/forks/karthik558/setup_hack_env?style=for-the-badge)
![](https://img.shields.io/github/stars/karthik558/setup_hack_env?style=for-the-badge)
![](https://img.shields.io/github/issues/karthik558/setup_hack_env?style=for-the-badge)
![](https://img.shields.io/github/languages/code-size/karthik558/setup_hack_env?style=for-the-badge)

![IMAGE](assets/script-linux.png)

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

- Set of tools I use to automate my daily tasks and for learning purposes.
- Included TP-LINK-722N wifi drivers. (check TP-LINK folder) (Instructions are given on #Usage-TP-LINK-722N)
- Tools are cloned/fetched from [Ethical-Hacking-Tools](https://github.com/Ethical-Hacking-Tools)

## Prerequisites

- Run the script with root privileges only (sudo).
- Download the full-font pack from [here](http://www.mediafire.com/file/on3q6yhfqzo4jh1/Fonts.zip/file) and extract it to /usr/share/fonts. [Note: This is optional]
- I haven't included a script to download burp-suite pro, but you can get it from here (https://t.me/burpsuite) (for bug-bounty hunters)

## Usage (Kali/ParrotOS)

1. `git clone https://github.com/karthik558/setup_hack_env.git`
2. `cd setup_hack_env`
3. `sudo python3 setup-hack.py`

## Usage (TP-LINK-722N)

1. `git clone https://github.com/karthik558/setup_hack_env`
2. `cd setup_hack_env && cd TP-LINK*`
3. `sudo python3 TP722N1.py`
4. After completing the process, reboot your pc, after rebooting, run the 2nd script.
5. `sudo python3 TP722N2.py`
6. After completing the process, reboot your pc again.
7. Finally after completing (script-1 & script-2) run the 3rd script to check if drivers are installed properly or not.
8. `sudo bash injection-test.sh`

## After Installation Fixes

1. For fixing font blank issues in system-wide then download this file and extract it to /usr/share/fonts/ or /usr/share/local/fonts/
```
wget http://www.mediafire.com/file/on3q6yhfqzo4jh1/Fonts.zip/file
unzip Fonts.zip
sudo mv Fonts /usr/share/fonts/
```

2. Fix Grub Resolution Issues

- Open the terminal and run the following command
```bash
sudo nano /etc/default/grub
``` 
- Find the line `GRUB_GFX_MODE="auto"` and replace it with `GRUB_GFX_MODE="1920x1080x32"`
- Save the file and run the following command
```bash 
sudo update-grub && sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot
```

3. Incase of grub-loader not showing any of your windows partition, then run the following command
```bash
sudo nano /etc/default/grub
```
- Add the line `GRUB_DISABLE_OS_PROBER=false` and save the file
- Run the following command
```bash
sudo update-grub && sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot
```

4. Remove the folder permission after installation
```bash
sudo chown -R $USER:$USER /usr/share/fonts/Fonts
```

5. Change the default shell to bash
```bash
chsh -s /bin/bash
```

6. Configure Proxychains
```bash 
sudo nano /etc/proxychains.conf
```
- Find the line `strict_chain` and comment it out by adding `#` at the beginning of the line
- Find the line `dynamic_chain` and uncomment it by removing `#` from the beginning of the line
- Add the following line at the end of the file
```
socks5 127.0.0.1 9050
```
- Save the file and exit
- sudo service tor start
- proxychains firefox www.google.com (to check if tor is working or not)

## Contributing

Contributions to the project are welcome. If you would like to suggest an improvement or report a bug, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).