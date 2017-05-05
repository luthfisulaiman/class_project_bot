from csuibot.utils import zodiac as z
from csuibot.utils import wiki
import wikipedia


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


def lookup_wiki(term):
    if term == '':
        raise ValueError('Command /wiki need an argument')
    else:
        object_wiki = wiki.Wiki(term)
        try:
            return object_wiki.get_result()
        except wikipedia.exceptions.PageError as e:
            raise IndexError(
                'Page id "' + term + '" does not match any pages.'
                ' Try another id!'
            )
