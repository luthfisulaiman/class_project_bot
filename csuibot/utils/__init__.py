from csuibot.utils import zodiac as z
from csuibot.utils import hangout
from random import randint


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


def get_nearest_hangout(user_long, user_lat):
    h_list = hangout.create_hangout_list()
    res = hangout.find_nearest_place(h_list, user_long, user_lat)
    str_msg = print_message(res['nearest'], res['n_dist'])
    return dict(message=str_msg, nearest=res['nearest'])


def get_random_hangout(amount):
    h_list = hangout.create_hangout_list()
    result = []

    while amount > 0:
        x = randint(0, len(h_list) - 1)
        tmp = h_list.pop(x)
        result.append(tmp)
        amount -= 1

    return result


def print_message(hangout_data, dist=None):
    str_msg = '[' + hangout_data.name + ']' + '\n'
    str_msg += 'Location: ' + '\n' + hangout_data.address + '\n'
    str_msg += 'Distance: ' + str(int(dist)) + ' metres' + '\n'
    return str_msg
