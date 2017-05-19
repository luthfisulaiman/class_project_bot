from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, create_schedule, get_schedules)
from telebot import types
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

    def date_schedule(date_message):

        def time_schedule(time_message):
            app.logger.debug("time of schedule is {}".format(time_message.text))
            print("{} {} {}".format(message.chat.id, date_message.text, time_message.text))
            result = create_schedule(message.chat.id, date_message.text, time_message.text)

        app.logger.debug("date of schedule is {}".format(date_message.text))

        try:
            y, m, d = parse_date(date_message.text)
            if datetime.date(y, m, d) >= datetime.datetime.now().date():
                markup = types.ReplyKeyboardMarkup()
                btn09 = types.KeyboardButton('09.00')
                btn10 = types.KeyboardButton('10.00')
                btn11 = types.KeyboardButton('11.00')
                btn12 = types.KeyboardButton('12.00')
                btn13 = types.KeyboardButton('13.00')
                btn14 = types.KeyboardButton('14.00')
                markup.add(btn09, btn10, btn11, btn12, btn13, btn14)
                msg = bot.send_message(date_message.from_user.id,
                                       'Here are the available hours for {}.'.format(
                                            date_message.text),
                                       reply_markup=markup)
                bot.register_next_step_handler(msg, time_schedule)
            else:
                msg = bot.reply_to(date_message,
                                   'You cannot make a schedule for the past. Try again.')
                bot.register_next_step_handler(msg, date_schedule)
        except ValueError:
            msg = bot.reply_to(date_message, 'The requested date is invalid. Try again.')
            bot.register_next_step_handler(msg, date_schedule)

    app.logger.debug("'create_schedule' command detected")
    msg = bot.send_message(message.from_user.id, 'When should the schedule be created?')
    bot.register_next_step_handler(msg, date_schedule)
