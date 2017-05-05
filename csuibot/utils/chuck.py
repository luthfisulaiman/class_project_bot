import requests as r

class Chuck:
    def __init__(self):
        self.url = "http://api.icndb.com/jokes/random"

    def get_chuck(self):
        return r.get(self.url)
