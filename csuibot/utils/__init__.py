from csuibot.utils import meme
from csuibot.utils import zodiac as z, hex2rgb as h, xkcd as x
from csuibot.utils import yelkomputer


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


def get_meme(top, bottom):
    generator = meme.MemeGenerator()
    generator.createid()
    try:
        generator.createtop(top)
        generator.createbottom(bottom)
    except ValueError:
        return 'Caption is too long, min < 100 words'
    else:
        dank = generator.generatememe()
        return dank.getimage()


def fetch_latest_xkcd():
    return x.Comic.get_latest_comic()


def convert_hex2rgb(hex_str):
    return h.Hex2RGB(hex_str).convert()


def lookup_yelkomputer(message_text):
    if message_text == '/yelkomputer':
        return yelkomputer.YelKomputer.get_yel_komputer()
    else:
        raise ValueError('Command /yelkomputer doesn\'t need any arguments')
