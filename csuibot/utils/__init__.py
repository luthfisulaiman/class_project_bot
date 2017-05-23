from csuibot.utils import zodiac as z
from bs4 import BeautifulSoup
import requests


def lookup_zodiac(month, day):
    zodiacs = [
        z.Aries(),
        z.Taurus(),
        z.Gemini(),
        z.Cancer(),
        z.Leo(),
        z.Virgo(),
        z.Libra(),
        z.Scorpio(),
        z.Sagittarius(),
        z.Capricorn(),
        z.Aquarius(),
        z.Pisces()
    ]

    for zodiac in zodiacs:
        if zodiac.date_includes(month, day):
            return zodiac.name
    else:
        return 'Unknown zodiac'


def lookup_chinese_zodiac(year):
    num_zodiacs = 12
    zodiacs = {
        0: 'rat',
        1: 'buffalo',
        2: 'tiger',
        3: 'rabbit',
        4: 'dragon',
        5: 'snake',
        6: 'horse',
        7: 'goat',
        8: 'monkey'
    }
    ix = (year - 4) % num_zodiacs

    try:
        return zodiacs[ix]
    except KeyError:
        return 'Unknown zodiac'
    

def lookup_album_price():
    album = requests.get('http://vgmdb.net/db/albums-search.php?do=results&action=upcoming')
    soup = BeautifulSoup(recent.text, "html.parser")
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
                total = satu * float(album_price[0])
                result += str(int(total)) + ' IDR\n'
            else:
                result += 'Tidak Dijual\n'
        i += 1
    return result
