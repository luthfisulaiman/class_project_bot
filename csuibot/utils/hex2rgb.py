import requests


class Hex2RGB:

    API_URL = 'http://thecolorapi.com/id?hex='

    def __init__(self, hex_str):
        self.hex = hex_str

    def convert(self):
        r = requests.get('{}{}'.format(self.API_URL, self.hex.strip('#')))

        # Based on thecolorapi. Format: 'RGB(R, G, B)'
        rgb = r.json()['rgb']['value'].upper()
        return rgb
