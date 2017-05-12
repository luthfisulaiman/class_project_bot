from csuibot.utils import message_dist as md
import json
import re
import time
from csuibot.utils import (zodiac as z, ip, palindrome as p, hipster as hp,
                           loremipsum as li, hex2rgb as h, xkcd as x, meme,
                           password as pw, custom_chuck as cc, kelaskata as k,
                           define as d, yelkomputer, soundcomposer as sc,
                           calculate_binary as cb, isupweb as iuw, notiftaker as n,
                           compute as co, definisi, note, dayofdate as dod,
                           chuck, discretemath as dm, marsfasilkom, yelfasilkom,
                           wiki)


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
        except Exception as e:
            raise IndexError(
                'Page id "' + term + '" does not match any pages.'
                ' Try another id!'
            )


def lookup_message_dist(chat_id):
    message_dist = md.get_message_dist()
    message_dist_text = ''
    total_message = 0

    for hour in range(0, 24):
        total_message += message_dist['dist'][str(chat_id)][str(hour)]

    for hour in range(0, 24):
        idx_hour = 0
        idx_percent = 0
        try:
            val = message_dist['dist'][str(chat_id)][str(hour)] * 100.0
            idx_percent = float(val) / total_message
        except ZeroDivisionError:
            percent_at_specified_hour = 0.0
            idx_hour = str(hour).zfill(2)
            idx_percent = str(round(percent_at_specified_hour, 2))
        message_dist_text += '{} -> {}%\n'.format(idx_hour, idx_percent)

    return message_dist_text


def add_message_dist(chat_id, hour):
    md.add_message_to_dist(chat_id, hour)


def lookup_marsfasilkom(message_text):
    if message_text == '/marsfasilkom':
        return marsfasilkom.MarsFasilkom.get_mars_fasilkom()
    else:
        raise ValueError('Command /marsfasilkom doesn\'t need any arguments')


def lookup_yelfasilkom(message_text):
    if message_text == '/yelfasilkom':
        return yelfasilkom.YelFasilkom.get_yel_fasilkom()
    else:
        raise ValueError('Command /yelfasilkom doesn\'t need any arguments')


def call_discrete_material(query):
    return dm.DiscreteMath().get_discrete_material(query)


def manage_notes(command, text=''):
    note_obj = note.Notes(text)

    if command == 'view':
        try:
            return note_obj.view()
        except (FileNotFoundError, json.JSONDecodeError):
            return 'No notes yet'
    elif command == 'add':
        return note_obj.write()


def lookup_definisi(word):
    kamus = definisi.Definisi()

    mean = kamus.define(word)

    return mean


def takescelenotif():

    notif = n.NotifTaker()
    return notif.getPost()


def lookup_isupweb(url):
    pattern = re.compile("^(https?)://[^\s/$.?#].[^\s]*$")
    if(pattern.match(url)):
        return iuw.IsUpWeb(url).isup()
    else:
        raise ValueError


def remind_me(second, text):
    s = int(second)
    if(s > 30):
        raise Exception
    while(s > 0):
        time.sleep(1)
        s -= 1
    return text


def calculate_binary(bina, operand, binb):
    if operand == '+':
        return str(cb.CalculateBinary(bina, binb).addition())
    elif operand == '-':
        return str(cb.CalculateBinary(bina, binb).subtraction())
    elif operand == '*':
        return str(cb.CalculateBinary(bina, binb).multiplication())
    else:
        return str(cb.CalculateBinary(bina, binb).division())


def lookup_define(word):
    if(not word):
        raise ValueError('Command /define need an argument')
    elif(containsdigit(word)):
        return word + ' contains number'
    else:
        define_object = d.Define(word)
        return define_object.getdefine()


def containsdigit(string):
    return any(i.isdigit() for i in string)


def lookup_kelaskata(message):
    if message == '':
        raise ValueError('Try /kelaskata [word]')
    else:
        kelaskata_object = k.Kelaskata(message)
        return kelaskata_object.getkelaskata()


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


def compute(message):
    _, text = message.text.split(' ')
    return co.Compute(text).calculate()


def call_composer(username):
    return sc.SoundComposer(username).get_composer()


def lookup_dayofdate(year, month, day):
    try:
        return dod.Dayofdate.dayoutput(year, month, day)
    except ValueError:
        return ('Incorrect use of dayofdate command. '
                'Please write a valid date in the form of yyyy-mm-dd, '
                'such as 2016-05-13')


def get_chuck(message_text):
    if message_text == "/chuck":
        return chuck.Chuck().get_chuck()
    else:
        raise ValueError('Command /chuck doesn\'t need any arguments')


def similar_text():
    raise NotImplemented
