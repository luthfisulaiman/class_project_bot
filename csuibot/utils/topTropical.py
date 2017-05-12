from xml.etree import ElementTree as ET
import requests


class topTropicalBb:
    def __init__(self):
        self.post = "top tropical bilboard"

    def getTopTropical(self):
        r = requests.get("http://www.billboard.com/rss/charts/tropical-songs")
        hasil = ET.fromstring(r.text)
        hasil = hasil[0][5][0]
        return hasil.text


tro = topTropicalBb()
print(tro.getTopTropical())
