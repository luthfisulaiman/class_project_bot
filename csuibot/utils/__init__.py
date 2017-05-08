from csuibot.utils import zodiac as z
from csuibot.utils import message_dist as md
from csuibot.utils import yelkomputer
import datetime

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

def lookup_message_dist(chat_id):
    message_dist = md.get_message_dist()
    message_dist_text = ''
    total_message = 0

    for hour in range(0, 24):
        total_message += message_dist['dist'][str(chat_id)][str(hour)]

    for hour in range(0, 24):
        try:
            percent_at_specified_hour = float(message_dist['dist'][str(chat_id)][str(hour)] * 100.0) / total_message
        except ZeroDivisionError:
            percent_at_specified_hour = 0.0
        message_dist_text += '{} -> {}%\n'.format(str(hour).zfill(2), str(round(percent_at_specified_hour, 2)))

    return message_dist_text

def add_message_dist(chat_id, hour):
    md.add_message_to_dist(chat_id, hour)

def lookup_yelkomputer(message_text):
    if message_text == '/yelkomputer':
        return yelkomputer.YelKomputer.get_yel_komputer()
    else:
        raise ValueError('Command /yelkomputer doesn\'t need any arguments')

