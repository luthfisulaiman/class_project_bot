import requests as r


class LoremIpsum:
    def __init__(self):
        self.url = "http://loripsum.net/api/1/short/plaintext"

    def get_loripsum(self):
        return r.get(self.url).text
