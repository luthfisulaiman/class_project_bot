from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, get_nearest_hangout,
                    get_random_hangout, get_hangout, print_message)

from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import os

request_hangout = -1
spec_dist = 0


@bot.message_handler(regexp=r'^/about$')
def help(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'CSUIBot v0.0.1\n\n'
        'Dari Fasilkom, oleh Fasilkom, untuk Fasilkom!'
    )
    bot.reply_to(message, about_text)


@bot.message_handler(regexp=r'^/zodiac \d{4}\-\d{2}\-\d{2}$')
def zodiac(message):
    app.logger.debug("'zodiac' command detected")
    _, date_str = message.text.split(' ')
    _, month, day = parse_date(date_str)
    app.logger.debug('month = {}, day = {}'.format(month, day))

    try:
        zodiac = lookup_zodiac(month, day)
    except ValueError:
        bot.reply_to(message, 'Month or day is invalid')
    else:
        bot.reply_to(message, zodiac)


@bot.message_handler(regexp=r'^/shio \d{4}\-\d{2}\-\d{2}$')
def shio(message):
    app.logger.debug("'shio' command detected")
    _, date_str = message.text.split(' ')
    year, _, _ = parse_date(date_str)
    app.logger.debug('year = {}'.format(year))

    try:
        zodiac = lookup_chinese_zodiac(year)
    except ValueError:
        bot.reply_to(message, 'Year is invalid')
    else:
        bot.reply_to(message, zodiac)


@bot.message_handler(regexp=r'^/hangout_kuy$')
def hangout_nearby(message):

    app.logger.debug("'hangout_kuy' command detected")
    str_msg = 'Tap to get your location and get nearby hangout place!'

    keyboard = KeyboardButton('Go!', request_location=True)
    reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_keyboard.add(keyboard)

    bot.send_message(chat_id=message.chat.id, text=str_msg, reply_markup=reply_keyboard)

    set_request_hangout(0)


@bot.message_handler(regexp=r'^/random_hangout_kuy$')
def hangout_random(message):

    app.logger.debug("'random_hangout_kuy$' command detected")
    str_msg = 'Tap to get your location and get random hangout place!'

    keyboard = KeyboardButton('Go!', request_location=True)
    reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_keyboard.add(keyboard)

    bot.send_message(chat_id=message.chat.id, text=str_msg, reply_markup=reply_keyboard)

    set_request_hangout(1)


@bot.message_handler(regexp=r'^/nearby_hangout_kuy \d+$')
def hangout_nearby_specified(message):

    app.logger.debug("'nearby_hangout_kuy' command detected")
    str_msg = 'Tap to get your location and get specified radius hangout place!'

    keyboard = KeyboardButton('Go!', request_location=True)
    reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_keyboard.add(keyboard)

    bot.send_message(chat_id=message.chat.id, text=str_msg, reply_markup=reply_keyboard)

    tmp_msg = message.split(' ')
    dist = int(tmp_msg[1])

    set_specified_distance(dist)
    set_request_hangout(2)


@bot.message_handler(regexp=r'^/hangout')
def hangout_keyboard(message):

    app.logger.debug("'hangout' command detected")

    tmp_msg = message.text.split(' ')
    msg = ''
    dist = ''

    for index, str_tmp in enumerate(tmp_msg):
        if index == 0:
            continue
        elif index == len(tmp_msg) - 1:
            dist = str_tmp
        else:
            msg = msg + ' ' + str_tmp

    res = get_hangout(msg[1:])

    nearest_path = '/utils/hangout_images/' + res.image_dir
    path = os.path.dirname(os.path.abspath(__file__)) + nearest_path
    bot.send_photo(message.chat.id, open(path, 'rb'))
    bot.reply_to(message, print_message(res, dist))


@bot.message_handler(content_types=['location'])
def get_nearest_location(message):

    loc = dict(latitude=message.location.latitude, longitude=message.location.longitude)
    req = get_request_hangout()

    try:
        if req == 0:
            res = get_nearest_hangout(loc['longitude'], loc['latitude'])
        elif req == 1:
            res = get_random_hangout(5)
        elif req == 2:
            res = get_nearest_hangout(loc['longitude'], loc['latitude'])
            sp_dist = get_specified_distance()

            if res['nearest'].distance > sp_dist:
                bot.reply_to(message, 'There is no hangout place within specified radius!')
                return

    except ValueError:
        bot.reply_to(message, 'input is invalid')

    else:
        if req == 0 or req == 2:
            nearest_path = '/utils/hangout_images/' + res['nearest'].image_dir
            path = os.path.dirname(os.path.abspath(__file__)) + nearest_path
            bot.send_photo(message.chat.id, open(path, 'rb'))
            bot.reply_to(message, res['message'])
        elif req == 1:

            str_msg = 'Choose one hangout place!'
            reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)

            for data in res:
                data.set_distance = data.set_distance(loc['longitude'], loc['latitude'])
                key_text = '/hangout ' + data.name + ' ' + str(int(data.distance))
                keyboard = KeyboardButton(text=key_text)
                reply_keyboard.add(keyboard)

            bot.send_message(chat_id=message.chat.id, text=str_msg,
                             reply_markup=reply_keyboard)

        set_request_hangout(-1)


def set_request_hangout(num):
    global request_hangout
    request_hangout = num


def get_request_hangout():
    return request_hangout


def set_specified_distance(num):
    global spec_dist
    spec_dist = num


def get_specified_distance():
    return spec_dist


def parse_date(text):
    return tuple(map(int, text.split('-')))
