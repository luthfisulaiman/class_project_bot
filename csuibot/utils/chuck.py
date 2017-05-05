import requests as r
import json
from pprint import pprint

class Chuck:
    def __init__(self):
        self.url = "http://api.icndb.com/jokes/random"

    def get_chuck(self):
        data = json.load(r.get(self.url))
