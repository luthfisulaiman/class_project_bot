from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, lookup_dayofdate
import datetime


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


def parse_date(text):
    return tuple(map(int, text.split('-')))


@bot.message_handler(regexp=r'^/dayofdate \d{4}\-\d{2}\-\d{2}$')
def dayofdate(message):
    app.logger.debug("'dayofdate' command detected")
    _, date_str = message.text.split(' ')
    year, month, day = parse_date(date_str)
    app.logger.debug('year = {}, month = {}, day = {}'.format(year, month, day))

    try:
        # check invalid date such as leap year, month 13 etc
        __newDate__ = datetime.datetime(year, month, day)
        dayofdate = lookup_dayofdate(year, month, day)
    except ValueError:
        bot.reply_to(message,
                     'Incorrect use of dayofdate command. '
                     'Please write a valid date in the form of yyyy-mm-dd, '
                     'such as 2016-05-13', __newDate__)
    else:
        bot.reply_to(message, dayofdate)


# invalid dayofdate calls
@bot.message_handler(regexp=r'^/dayofdate (?!\d{4}\-\d{2}\-\d{2}).*$')
def invalid_dayofdate(message):
    app.logger.debug("invalid 'dayofdate' command detected")
    bot.reply_to(message,
                 'Incorrect use of dayofdate command. '
                 'Please write a valid date in the form of yyyy-mm-dd, '
                 'such as 2016-05-13')
