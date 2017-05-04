import urllib.request

class IP:

    def ip(self):
        return urllib.request.urlopen("https://api.ipify.org").read()
