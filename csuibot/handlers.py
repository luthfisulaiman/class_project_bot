from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, generate_custom_chuck_joke


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


@bot.message_handler(regexp=r'^/chuck \d+ \d+$')
def custom_chuck_joke(message):
    app.logger.debug("'chuck' command detected")
    _, first_name, last_name = message.text.split(' ')
    app.logger.debug("first = {}, last = {}".format(first_name, last_name))

    try:
        joke = generate_custom_chuck_joke(first_name, last_name)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to icndb.com API, please try again later.')
    else:
        bot.reply_to(message, joke)


def parse_date(text):
    return tuple(map(int, text.split('-')))
