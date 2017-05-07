from csuibot.utils import zodiac as z
from csuibot.utils import kelaskata as k

from csuibot.utils import define as d


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


def lookup_define(word):
    if(not word):
        raise ValueError('Command /define need an argument')
    elif(containsDigit(word)):
        return word + ' contains number'
    else:
        define_object = d.define(word)
        return define_object.getDefine()


def containsDigit(string):
    return any(i.isdigit() for i in string)


def lookup_kelaskata(message):
    if message == '':
        raise ValueError('Try /kelaskata [word]')
    else:
        kelaskata_object = k.kelaskata(message)
        return kelaskata_object.getKelasKata()
