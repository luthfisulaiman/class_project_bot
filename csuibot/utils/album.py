from bs4 import BeautifulSoup
from datetime import datetime
import requests


class Facade:

    def __init__(self):
        self._subsystem = Album()
        

    def operation(self):
        self._subsystem.operation()


class Album:

    def operation(self):
        BASE_URL = "http://vgmdb.net/db/albums-search.php?do=results&action=upcoming"
        album = requests.get(BASE_URL)
        soup = BeautifulSoup(album.text, "html.parser")
        title = soup.find_all('span', {'class': 'albumtitle', 'lang': 'en'})
        date = soup.find_all('td', {'style': 'padding: 4px; font-size:9pt; text-align: right'})
        result = ''
        i = 0
        this_month = str(datetime.now().month)
        album_date = date[0].next['href'][33]
        while i < len(title) and (this_month == album_date):
            album_date = date[i].next['href'][33]
            album_title = title[i].text
            if ('original' and 'soundtrack' in album_title.lower()):
                result += album_title + ' : '
                prices = soup.find_all('a', {'title': album_title})
                album_url = prices[0]['href']
                detail = requests.get(album_url)
                beautiful = BeautifulSoup(detail.text, 'html.parser')
                arr = beautiful.find_all('td')
                album_price = arr[16].text.split(' ')
                if (album_price[0].split('.')[0].isdigit()):
                    url = 'https://www.mataf.net/id/currency/converter-'
                    kurs = requests.get(url + album_price[1] + '-IDR?m1=' + album_price[0])
                    beautiful = BeautifulSoup(kurs.text, 'html.parser')
                    one_hundred = beautiful.find_all('input')[1]['value']
                    one = float(one_hundred)/100
                    total = one * float(album_price[0])
                    result += str(int(total)) + ' IDR\n'
                else:
                    result += 'Tidak Dijual\n'
            i += 1
        return result
