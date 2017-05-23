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
        chart_item_title = xmldoc.getElementsByTagName('chart_item_title')
        result = ""
        index = 0
        for i in artists:
            if(i.firstChild.nodeValue.lower() == self.message.lower()):
                rank = ranks[index].firstChild.nodeValue
                artist = artists[index].firstChild.nodeValue
                title = chart_item_title[index].firstChild.nodeValue
                result += artist + "\n" + title + '\nRank #' + rank + "\n"
            index += 1
        if(result == ""):
            return self.message + " doesn't exist in bill200"
        else:
            return result[:-1]
