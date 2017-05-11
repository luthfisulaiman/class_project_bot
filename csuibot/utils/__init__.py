from csuibot.utils import (zodiac as z, ip, palindrome as p, hipster as hp,
                           loremipsum as li, hex2rgb as h, xkcd as x, meme,
                           password as pw, custom_chuck as cc, kelaskata as k,
                           define as d, hotcountry as hot, newage as na)
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


def generate_custom_chuck_joke(first_name, last_name):
    return cc.CustomChuckJoke().generate_custom_chuck_joke(first_name, last_name)


def generate_password(len):
    return pw.Password().generate_password(len)


def get_public_ip():
    return ip.IP().ip()


def make_hipster(paras):
    generator = hp.HipsterGenerator()

    try:
        return generator.generate(paras)
    except ValueError:
        return 'Number of paragraph exceed the limit'


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


def check_palindrome(message):
    _, text = message.text.split(' ')
    return p.Palindrome(text).is_palindrome()


def call_lorem_ipsum():
    return li.LoremIpsum().get_loripsum()


def fetch_latest_xkcd():
    return x.Comic.get_latest_comic()


def convert_hex2rgb(hex_str):
    return h.Hex2RGB(hex_str).convert()


def lookup_yelkomputer(message_text):
    if message_text == '/yelkomputer':
        return yelkomputer.YelKomputer.get_yel_komputer()
    else:
        raise ValueError('Command /yelkomputer doesn\'t need any arguments')


def lookup_hotcountry():
    hotcountry_object = hot.hotcountry()
    return hotcountry_object.getHotcountry()


def lookup_newage():
    newage_object = na.newage()
    return newage_object.getNewage()
