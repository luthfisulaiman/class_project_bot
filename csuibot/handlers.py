from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, generate_schedule,
                    get_available_schedules, get_schedules)
from telebot import types
import datetime


schedules = {}


class EntrySchedule:
    def __init__(self, group):
        self.group = group
        self.date = None
        self.time = None


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
    entry = EntrySchedule(message.chat.id)
    schedules[message.from_user.id] = entry
    msg = bot.send_message(message.from_user.id, 'When should the schedule be created?')
    bot.register_next_step_handler(msg, date_schedule)


def date_schedule(date_message):
    app.logger.debug("date of schedule step started")
    if date_message.text == '/cancel':
        schedules.pop(date_message.from_user.id)
        bot.reply_to(date_message, 'create_schedule canceled.')
        return

    try:
        y, m, d = parse_date(date_message.text)
        if datetime.date(y, m, d) >= datetime.datetime.now().date():
            entry = schedules[date_message.from_user.id]

            avl_hours = get_available_schedules(entry.group, date_message.text)
            avl_hours.sort()
            if len(avl_hours) <= 0:
                error_text = "That date's full. Try another date or use /cancel to cancel."
                msg = bot.reply_to(date_message, error_text)
                bot.register_next_step_handler(msg, date_schedule)
                return

            app.logger.debug("date of schedule is {}".format(date_message.text))
            entry.date = date_message.text
            markup = types.ReplyKeyboardMarkup()
            for avl_hour in avl_hours:
                markup.add(types.KeyboardButton("{}.00".format(avl_hour)))
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


def time_schedule(time_message):
    app.logger.debug("time of schedule started")
    if time_message.text == '/cancel':
        schedules.pop(time_message.from_user.id)
        bot.reply_to(time_message, 'create_schedule canceled.')
        return

    app.logger.debug("time of schedule is {}".format(time_message.text))
    entry = schedules[time_message.from_user.id]
    entry.time = time_message.text.split('.')[0]
    msg = bot.reply_to(time_message, 'Give a description for this schedule.',
                       reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, desc_schedule)


def desc_schedule(desc_message):
    app.logger.debug("desc of schedule started")
    if desc_message.text == '/cancel':
        schedules.pop(desc_message.from_user.id)
        bot.reply_to(desc_message, 'create_schedule canceled.')
        return

    app.logger.debug("desc of schedule is {}".format(desc_message.text))
    entry = schedules[desc_message.from_user.id]
    generate_schedule(entry.group, entry.date, entry.time, desc_message.text)
    bot.reply_to(desc_message, 'Schedule created successfully.')
    bot.send_message(entry.group, 'A schedule has been created.')
    bot.send_message(entry.group,
                     "{} jam {}.00: {}".format(entry.date, entry.time, desc_message.text))
    schedules.pop(desc_message.from_user.id)
