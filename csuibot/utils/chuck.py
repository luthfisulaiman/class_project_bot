import requests as r
import html

class Chuck:
    def __init__(self):
        self.url = "http://api.icndb.com/jokes/random"

    def get_chuck(self):
        return html.unescape(r.get(self.url).json()['value']['joke'])
