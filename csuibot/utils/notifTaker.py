from bs4 import BeautifulSoup
import urllib.request


class notifTaker:
    def __init__(self):
        self.post = "notif"

    def makeNotifReport(self, subject, info, post):
        laporan = ""
        counter = 0
        subLaporan = ""
        for judul in subject:
            subLaporan = subject[counter].contents[0].upper() + info[counter] + "\n"
            subLaporan += post[counter]
            subLaporan += "\n \n scele.cs.ui.ac.id \n =================================== \n"
            laporan += subLaporan
            counter += 1
        return laporan

    def getPost(self):
        r = urllib.request.urlopen("https://scele.cs.ui.ac.id/").read()
        soup = BeautifulSoup(r, "html.parser")
        subject = soup.find_all("div", class_="subject")
        info = soup.find_all("div", class_="author")
        post = soup.find_all("div", class_="posting")
        flagNavString = type(post[1].contents[0].contents[0])
        infoJadi = self.olahInfo(info)
        postJadi = self.olahPost(post, flagNavString)
        return self.makeNotifReport(subject, infoJadi, postJadi)

    def olahInfo(self, arrayInfo):
        arrayHasil = []
        for element in arrayInfo:
            hasil = " "
            hasil += (element.contents[0]+element.contents[1].contents[0].upper())
            hasil += (" ("+element.contents[2][2:]+")")
            arrayHasil.append(hasil)
        return arrayHasil

    def olahPost(self, arrayInfo, flagNavString):
        arrayHasil = []
        for element in arrayInfo:
            hasil = ""
            for subcontainer in element:
                for subelement in subcontainer:
                    if(type(subelement) == flagNavString):
                        hasil += subelement
                    else:
                        hasil += "\n"
            arrayHasil.append(hasil)
        return arrayHasil


notifTakera = notifTaker()
notifTakera.getPost()
