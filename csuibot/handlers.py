from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, get_aqi_coord, get_aqi_city
import re


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


@bot.message_handler(commands=['aqi'])
def air_quality(message):
    app.logger.debug("'aqi' command detected")
    arr_loc = message.text.split(' ', 1)

    if(len(arr_loc) > 1 and not arr_loc[1].isspace() and len(arr_loc[1]) > 0):
        loc = arr_loc[1]

        if(re.match(r'^(\d+[.]?\d+|\d) (\d+[.]?\d+|\d)$', loc)):
            try:
                result = get_aqi_coord(loc)
            except ConnectionError:
                bot.reply_to(message, "Unable to connect to aqicn.org, please try again later")
            else:
                bot.reply_to(message, result)

        elif (re.match(r'^[a-zA-Z0-9\s]*$', loc)):
            try:
                result = get_aqi_city(loc)
            except ConnectionError:
                bot.reply_to(message, "Unable to connect to aqicn.org, please try again later")
            else:
                bot.reply_to(message, result)

    else:
        bot.reply_to(message, "Invalid city name or coordinate, please try again")


def parse_date(text):
    return tuple(map(int, text.split('-')))
