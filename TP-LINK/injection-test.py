import os
import time

RED = '\033[31m'
GREEN = '\033[32m'
NC = '\033[0m'

# Let's start the script with a banner
def display_banner():

    banner =     "██╗   ████████╗███████╗███████╗████████╗/n"
    banner +=    "██║   ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝/n"
    banner +=    "██║█████╗██║   █████╗  ███████╗   ██║/n"
    banner +=    "██║╚════╝██║   ██╔══╝  ╚════██║   ██║/n"
    banner +=    "██║      ██║   ███████╗███████║   ██║/n"
    banner +=    "╚═╝      ╚═╝   ╚══════╝╚══════╝   ╚═╝/n"
    
display_banner()

# Terminal header settings and information
print(f"{RED}Developer   :   KARTHIK LAL (https://karthiklal.live){NC}")
print(f"{RED}Created Date:   2021-12-07{NC}")
print(f"{RED}Project     :   INJECTION-TEST{NC}")
print(f"{RED}Purpose     :   INJECTION-TEST{NC}")
print()

# Abort the script if the user is not root
print("Checking if you are running this script on su mode or not")
if not os.geteuid() == 0:
    print(f"{RED}This script must be run as root{NC}")
    time.sleep(1)
    exit()
else:
    print(f"{GREEN}You are running this script on su mode{NC}")
    time.sleep(1)
    os.system("clear")
    
# List available wireless adapters
os.system('iwconfig')

# Prompt user to select a wireless adapter
adapter = input('Enter the name of the wireless adapter to test (e.g. wlan0): ')

# Test packet-injection on the selected adapter
print(f'{RED}Starting the injection test on {adapter}...{NC}')
os.system(f'sudo ifconfig {adapter} down')
os.system(f'sudo iwconfig {adapter} mode monitor')
os.system(f'sudo ifconfig {adapter} up')
os.system(f'sudo iwconfig {adapter}')
print(f'{GREEN}Injecting packets on {adapter}...{NC}')
result = os.system(f'sudo aireplay-ng --test {adapter}')
if result == 0:
    print(f'{GREEN}Packet injection test done on {adapter} and it\'s working fine.{NC}')
else:
    print(f'{RED}Packet injection test failed on {adapter}.{NC}')

# Press enter to exit
print(f"{GREEN}Press enter to exit{NC}")
