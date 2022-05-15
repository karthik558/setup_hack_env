![HEADER_IMAGE](assets/script-linux.png)
```
- ABOUT THIS SCRIPT -

* Set of scripts to clone all tools that i use on my kali-linux.

* Included TP-LINK-722N wifi drivers. (check TP-LINK DRIVER folder) (run it according to there file-name).

* Tool's are cloned/fetched from (https://github.com/Ethical-Hacking-Tools).

- NOTES/INSTRUCTIONS -

* Run script on (sudo su mode).

* Apply (Font & GRUB) path manually.

* Don't forgot to remove folder permission at last (this caused because we run the script on (sudo mode)).

* I haven't included script to download burp-suite pro (if you want it then , check this group for latest release , https://t.me/burpsuite)
```

```
- HOW TO USE THIS SCRIPT ? -

- git clone https://github.com/karthik558/setup_kali_env
- cd setup_kali_env
- chmod +x setup-kali.sh
- bash setup-kali.sh` OR DO `./setup-kali.sh
```
```
- HOW TO USE TP-LINK DRIVER SCRIPT ? -

- git clone https://github.com/karthik558/setup_kali_env
- cd setup_kali_env && cd TP-LINK*
- chmod *
- ./TP-LINK-WN722N(1).sh or bash TP-LINK-WN722N(1).sh (after completing, restart PC)
- After restarting PC, run this ./TP-LINK-WN722N(2).sh or bash TP-LINK-WN722N(2).sh
- Finally after completing (1 & 2) run injection-test.sh (for checking if drivers are installed properly or not)
```