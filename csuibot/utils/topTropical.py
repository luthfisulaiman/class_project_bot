from xml.etree import ElementTree as ET
import requests


class topTropicalBb:
    def __init__(self):
        self.post = "top tropical bilboard"

    def checkTopTropical(self, artist):
        r = requests.get("http://www.billboard.com/rss/charts/tropical-songs")
        hasil = ET.fromstring(r.text)
        printa = ""
        isInChart = False
        for i in range(4, 15):
            cur = hasil[0][i][2].text
            if cur.lower() == artist.lower():
                printa = cur + "\n"
                strArr = hasil[0][i][0].text.split()
                for x in range(1, len(strArr)):
                    printa = printa + strArr[x]+" "
                printa = printa + "\n" + strArr[0] + " Out of 10"
                isInChart = True
        if(isInChart):
            return printa
        else:
            return "Artist is not in the chart"
