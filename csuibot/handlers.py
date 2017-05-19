from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, get_schedules)


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


@bot.message_handler(func=lambda message: message.chat.type == "group", regexp="jadwal")
def jadwal(message):
    app.logger.debug("'jadwal' command detected")
    future_schedules = get_schedules(message.chat.id)
    if len(future_schedules) > 0:
        for schedule in future_schedules:
            bot.send_message(message.chat.id, schedule)
    else:
        bot.send_message(message.chat.id, 'No future schedules are found.')


@bot.message_handler(commands=['create_schedule'],
                     func=lambda message: message.chat.type == "group")
def create_schedule(message):
    app.logger.debug("'create_schedule' command detected")
    pass


def date_of_schedule(message):
    app.logger.debug("date of schedule is {}".format(message))
    pass


def time_of_schedule(message):
    app.logger.debug("time of schedule is {}".format(message))
    pass
