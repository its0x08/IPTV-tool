from requests import get
from urlparse import urlparse
from duckduckgo import search
from sys import argv

def extractUrls(dorks):
	temp = []
	for dork in open(dorks, "r").readlines():
		for link in search(dork.strip(), max_results=400):
			if link not in temp:
				temp.append(link)
	return temp

def checkUrls(urls):
	temp = []
	for url in urls:
		url = urlparse(url.strip())[1]
		if url not in temp:
			temp.append(url)
	print(f"[i] Found {len(temp)} in total.")
	return temp


def aliveOrNot(urls):
	temp = []
	print("[*] Hunting URLs for Admin panel")
	for url in urls:
		try:
			if "Xtream Codes</a>" in get(f"http://{url}/", timeout=10).text:
				print(f"\t{len(temp+1)} Panel found on URL  -->> http://{url}/")
				temp.append(url)
		except Exception as e:
			# print(f"\tNo Panel found -->> http://{url}/")
			pass
	print(f"[i] {len(temp)} of them are alive!")
	f = open("urls.txt", "a+")
	for url in temp:
		f.write(f"http://{url}/\n")
	f.close()

if __name__ == '__main__':
	try:
		dorks = argv[1]
		aliveOrNot(checkUrls(extractUrls(dorks)))
	except Exception as e:
		print(e)