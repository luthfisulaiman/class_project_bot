from csuibot.utils import zodiac as z
from csuibot.utils import message_dist as md
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

def lookup_message_dist(group_id):
    m = md.MessageDist()
    result = m.get_message_dist(group_id)
    message_dist = ''

    if result is None:
        return "Connection error"
    for key, value in result.items():
        message_dist += '{} -> {} \n'.format(key, value['percentage'])
    if message_dist == '':
        message_dist = 'Unknown error'
    return message_dist

def lookup_yelkomputer(message_text):
    if message_text == '/yelkomputer':
        return yelkomputer.YelKomputer.get_yel_komputer()
    else:
        raise ValueError('Command /yelkomputer doesn\'t need any arguments')
