from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, get_schedules)
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
    app.logger.debug("'create_schedule' command detected")
    msg = bot.send_message(message.from_user.id, 'When should the schedule be created?',
                           reply_markup=types.ForceReply())
    bot.register_next_step_handler(msg, date_schedule)


def date_schedule(message):
    app.logger.debug("date of schedule is {}".format(message.text))

    try:
        y, m, d = parse_date(message.text)
        if datetime.date(y, m, d) >= datetime.datetime.now().date(): #input date is correct
            markup = types.ReplyKeyboardMarkup()
            btn09 = types.KeyboardButton('{} jam 09'.format(message.text))
            btn10 = types.KeyboardButton('{} jam 10'.format(message.text))
            btn11 = types.KeyboardButton('{} jam 11'.format(message.text))
            btn12 = types.KeyboardButton('{} jam 12'.format(message.text))
            btn13 = types.KeyboardButton('{} jam 13'.format(message.text))
            btn14 = types.KeyboardButton('{} jam 14'.format(message.text))
            markup.add(btn09, btn10, btn11, btn12, btn13, btn14)
            msg = bot.send_message(message.from_user.id,
                                   'When should the schedule be created?',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, time_schedule)
        else: #input date is for the past
            msg = bot.reply_to(message, 'You cannot make a schedule for the past. Try again.',
                               reply_markup=types.ForceReply())
            bot.register_next_step_handler(msg, date_schedule)
    except ValueError: #input date is not a date
        msg = bot.reply_to(message, 'The requested date is invalid. Try again.',
                           reply_markup=types.ForceReply())
        bot.register_next_step_handler(msg, date_schedule)


def time_schedule(message):
    app.logger.debug("time of schedule is {}".format(message))
    print('you made it here')
