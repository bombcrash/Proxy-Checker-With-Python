import requests
from colorama import init, Fore, Style
from tkinter.filedialog import askopenfilename
from concurrent.futures import ThreadPoolExecutor
import urllib3
import sys

# Disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init()

# Test URL
test_url = "https://www.example.com"

# GUI call to select the file
file_path = askopenfilename(filetypes=[("Text Files", "*.txt")])

# File to store valid proxies
valid_proxies_file = "valid_proxies.txt"

# Update the test_proxy function
def test_proxy(proxy_url):
    try:
        response = requests.get(test_url, proxies={"http": proxy_url, "https": proxy_url}, timeout=10, verify=False)
        if response.status_code == 200:
            print(f"{Style.BRIGHT}{Fore.GREEN}Valid Proxy | {proxy_url}{Style.RESET_ALL}")
            with open(valid_proxies_file, "a") as valid_file:
                valid_file.write(proxy_url + "\n")
        else:
            print(f"{Style.BRIGHT}{Fore.RED}Invalid Proxy | {proxy_url}{Style.RESET_ALL}")
    except requests.exceptions.RequestException:
        print(f"{Style.BRIGHT}{Fore.RED}Invalid Proxy | {proxy_url}{Style.RESET_ALL}")

# Read the selected file and get proxies
with open(file_path, "r") as file:
    proxies = file.read().splitlines()

# Perform test for each proxy
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(test_proxy, proxies)

# Report the result
print("\nProxy check completed.", file=sys.stderr)