import requests as r
import html


class CustomChuckJoke:

    def __init__(self):
        self.url = "http://api.icndb.com/jokes/random"

    def generate_custom_chuck_joke(self, first_name, last_name):
        payload = {"firstName": first_name, "lastName": last_name}
        return html.unescape(r.get(self.url, params=payload).json()['value']['joke'])
