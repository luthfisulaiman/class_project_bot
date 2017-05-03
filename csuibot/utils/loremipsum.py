import requests as r


class LoremIpsum:
    def __init__(self):
        self.url = "http://loripsum.net/generate.php"
        self.num_par = 1
        self.length = "medium"

    def get_loripsum(self):
        payload = {"p": self.num_par, "l": self.length}
        return r.get(self.url, params=payload).text
