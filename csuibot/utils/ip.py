import requests as r


class IP:
    def __init__(self):
        self.url = "https://api.ipify.org"

    def ip(self):
        return r.get(self.url).text
