import datetime
import time
import math


class Weton:
    def __init__(self, year, month, day):
        self.date = datetime.date(year, month, day)

    def get_weton(self):
        hari = self.date.weekday()

        if hari == 0:
            hari = "Senin"
        elif hari == 1:
            hari = "Selasa"
        elif hari == 2:
            hari = "Rabu"
        elif hari == 3:
            hari = "Kamis"
        elif hari == 4:
            hari = "Jumat"
        elif hari == 5:
            hari = "Sabtu"
        else:
            hari = "Minggu"

        inisial = datetime.date(1970, 1, 2)
        inisial = int(time.mktime(inisial.timetuple())) * 1000

        tanggal_lahir = self.date
        tanggal_lahir = int(time.mktime(tanggal_lahir.timetuple())) * 1000

        hasil_bagi = ((tanggal_lahir - inisial) + 86400000) / 432000000
        sisa = round((hasil_bagi - math.floor(hasil_bagi)) * 10) / 2

        if sisa == 0:
            pasaran = "Wage"
        elif sisa == 1:
            pasaran = "Kliwon"
        elif sisa == 2:
            pasaran = "Legi"
        elif sisa == 3:
            pasaran = "Pahing"
        else:
            pasaran = "Pon"

        return hari + " " + pasaran
