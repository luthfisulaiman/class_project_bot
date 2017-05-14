import requests as r
from xml.dom import minidom


class billArtist:
    def __init__(self, message):
        self.webservice = "http://www.billboard.com/rss/charts/billboard-200"
        self.message = message

    def getBillArtist(self):
        res = r.get(self.webservice)
        xmldoc = minidom.parseString(res.text)
        ranks = xmldoc.getElementsByTagName('rank_this_week')
        artists = xmldoc.getElementsByTagName('artist')
        titles = xmldoc.getElementsByTagName('title')
        i = getArtistIndex(artists, self.message)
        if(i == -1):
            return self.message + " doesn't exist in bill200"
        else:
            rank = ranks[i].firstChild.nodeValue
            artist = artists[i].firstChild.nodeValue
            title = titles[i+1].firstChild.nodeValue
            title = title.split(":")
            titles = ""
            for str in title[1:-1]:
                titles += str + ":"
            titles += title[len(title)-1]
            return artist + "\n" + titles[1:] + '\nRank #' + rank


def getArtistIndex(artist, name):
    index = 0
    for i in artist:
        if(i.firstChild.nodeValue.lower() == name.lower()):
            return index
        index += 1
    return -1
