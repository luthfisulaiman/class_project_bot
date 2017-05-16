from bs4 import BeautifulSoup
import urllib.request
import urllib.error


class mangaTopOricon:
    def __init__(self):
        self.post = "10Manga"

    def getTopManga(self, year, month, day):
        if(len(month) < 2):
            month = "0" + month
        if(len(day) < 2):
            day = "0" + day
        l = "http://www.oricon.co.jp/rank/obc/w/" + year + "-" + month + "-" + day + "/"
        r = urllib.request.urlopen(l)
        soup = BeautifulSoup(r, "html.parser")
        judul = soup.find_all("h2", class_="title")[:10]
        author = soup.find_all("p", class_="name")[:10]
        hasil = ""
        for i in range(0, 10):
            hasil = hasil + "(" + str(i+1) + ") " + judul[i].text+" - "
            hasil = hasil + author[i].text+" \n"
        return hasil

    def getTopMangaMonthly(self, year, month):
        if(len(month) < 2):
            month = "0" + month
        l = "http://www.oricon.co.jp/rank/cbm/m/" + year + "-" + month+"/"
        r = urllib.request.urlopen(l)
        soup = BeautifulSoup(r, "html.parser")
        stl = "font-weight:bold; margin-bottom:2px; margin-top:2px;"
        judul = soup.find_all("li", {"style": stl})[:10]
        author = soup.find_all("li", class_="artist-name")[:10]
        hasil = ""
        for i in range(0, 10):
            hasil = hasil + "(" + str(i+1) + ") " + judul[i].text+" - "
            hasil = hasil + author[i].text+" \n"
        return hasil
