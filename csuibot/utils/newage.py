import requests as r
from xml.dom import minidom


class newage:
    def __init__(self):
        self.webservice = "http://www.billboard.com/rss/charts/new-age-albums"

    def getNewage(self):
        res = r.get(self.webservice)
        xmldoc = minidom.parseString(res.text)
        result = ""
        ranks = xmldoc.getElementsByTagName('rank_this_week')
        artists = xmldoc.getElementsByTagName('artist')
        titles = xmldoc.getElementsByTagName('title')
        title = ""
        for i in range(0, 10):
            rank = ranks[i].firstChild.nodeValue
            artist = artists[i].firstChild.nodeValue
            title = titles[i+1].firstChild.nodeValue
            title = title.split(":")
            result += '(' + rank + ') ' + artist + ' - ' + title[1][1:] + '\n'
        return result[0:len(result)-1]
