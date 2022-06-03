# -*- coding: utf-8 -*-
"""Scrapping module"""
from sys import argv

from duckduckgo import search
from requests import get
from requests.exceptions import HTTPError
from urlparse import urlparse


def extract_urls(dork_file):
    """Extractor function"""
    temp = []
    with open(dork_file, "r", encoding="utf8").readlines() as dorks_file:
        for dork in dorks_file:
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
    """Availability checker"""
    temp = []
    print("[*] Hunting URLs for Admin panel")
    for url in urls:
        try:
            if "Xtream Codes</a>" in get(f"http://{url}/", timeout=10).text:
                print(f"\t{len(temp+1)} Panel found on URL  -->> http://{url}/")
                temp.append(url)
        except HTTPError as not_iptv:
            print(not_iptv)
    print(f"[i] {len(temp)} of them are alive!")
    with open("urls.txt", "a+", encoding="utf-8") as url_file:
        for url in temp:
            url_file.write(f"http://{url}/\n")
        url_file.close()

if __name__ == '__main__':
    try:
        dorks = argv[1]
        alive_or_not(check_urls(extract_urls(dorks)))
    except HTTPError as err:
        print(err)
