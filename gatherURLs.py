try:
    from requests import get
    from urlparse import urlparse
    from duckduckgo import search
    from sys import argv
except ImportError as e:
    print str(e)

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
    print "[i] Found %s in total." % (len(temp))
    return temp


def aliveOrNot(urls):
    temp = []
    print "[*] Hunting URLs for Admin panel"
    for url in urls:
        try:
            if "Xtream Codes</a>" in get("http://%s/" % (url), timeout=10).text:
                print "\t{%s} Panel found on URL  -->> http://%s/" % (len(temp+1),url)
                temp.append(url)
        except Exception as e:
            # print "\tNo Panel found -->> http://%s/" %(url)
            pass
    print "[i] %s of them are alive!" % (len(temp))
    f = open("urls.txt", "a+")
    for url in temp:
        f.write("http://%s/\n" %(url))
    f.close()

if __name__ == '__main__':
    try:
        dorks = argv[1]
        aliveOrNot(checkUrls(extractUrls(dorks)))
    except Exception as e:
        print "Error\n%s" % (str(e))
