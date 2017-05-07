from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac
from .utils import manage_notes


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


@bot.message_handler(regexp=r'^/notes .*$')
def note(message):
    if message.text.find(' ') != -1:
        text = message.text.split(' ', 1)
        reply = ''

        if text[1] == 'view':
            try:
                reply = manage_notes('view')
            except FileNotFoundError:
                reply = 'No notes yet'
        else:
            reply = manage_notes('add', text[1])

        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, 'Usage :\n' +
                              '1. /notes view : View note in this group\n' +
                              '2. /notes [text] : Add new note in this group\n')


def parse_date(text):
    return tuple(map(int, text.split('-')))
