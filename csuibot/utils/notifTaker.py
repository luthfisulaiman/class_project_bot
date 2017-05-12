from bs4 import BeautifulSoup
import urllib.request


class NotifTaker:
    def __init__(self):
        self.post = "notif"

    def makenotifreport(self, subject, info, post, detail):
        laporan = ""
        counter = 0
        sublaporan = ""
        for judul in subject:
            sublaporan = subject[counter].contents[0].upper() + info[counter] + "\n"
            sublaporan += post[counter]
            sublaporan += "\n \n " + detail[counter] + "\n ================================ \n"
            laporan += sublaporan
            counter += 1
        return laporan

    def getpost(self):
        r = urllib.request.urlopen("https://scele.cs.ui.ac.id/").read()
        det = urllib.request.urlopen("https://scele.cs.ui.ac.id/mod/forum/view.php?f=1").read()
        soup = BeautifulSoup(r, "html.parser")
        detailedsoup = BeautifulSoup(det, "html.parser")
        subject = soup.find_all("div", class_="subject")
        info = soup.find_all("div", class_="author")
        post = soup.find_all("div", class_="posting")
        flagnavstring = type(post[1].contents[0].contents[0])
        detailjadi = self.olahdetail(detailedsoup)
        infojadi = self.olahinfo(info)
        postjadi = self.olahpost(post, flagnavstring)
        return self.makenotifreport(subject, infojadi, postjadi, detailjadi)

    def olahdetail(self, soup):
        outercontainer = soup.select('td.topic.starter')[:5]
        # only getting the first 5 (or according to scele front page)
        arrayhasil = []
        for element in outercontainer:
            hasil = ""
            hasil = element.a["href"]
            arrayhasil.append(hasil)
        return arrayhasil

    def olahinfo(self, arrayinfo):
        arrayhasil = []
        for element in arrayinfo:
            hasil = " "
            hasil += (element.contents[0]+element.contents[1].contents[0].upper())
            hasil += (" ("+element.contents[2][2:]+")")
            arrayhasil.append(hasil)
        return arrayhasil

    def olahpost(self, arrayinfo, flagnavstring):
        arrayhasil = []
        for element in arrayinfo:
            hasil = ""
            for subcontainer in element:
                for subelement in subcontainer:
                    if(type(subelement) == flagnavstring):
                        hasil += subelement
                    else:
                        hasil += "\n"
            arrayhasil.append(hasil)
        return arrayhasil


notiftakera = NotifTaker()
notiftakera.getpost()
