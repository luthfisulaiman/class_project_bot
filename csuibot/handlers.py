from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, lookup_yelkomputer, lookup_message_dist, add_message_dist
import datetime

def message_decorator(func):
    def wrapper(message):
        now = datetime.datetime.now()
        #using heroku timezone
        hour = (now.hour + 7) % 24
        chat_id = message.chat.id
        add_message_dist(chat_id, hour)
        return func(message)
    return wrapper


@bot.message_handler(regexp=r'^/about$')
@message_decorator
def help(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'CSUIBot v0.0.1\n\n'
        'Dari Fasilkom, oleh Fasilkom, untuk Fasilkom!'
    )
    bot.reply_to(message, about_text)


@bot.message_handler(regexp=r'^/zodiac \d{4}\-\d{2}\-\d{2}$')
@message_decorator
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
@message_decorator
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

@bot.message_handler(regexp=r'^/message_dist')
@message_decorator
def message_dist(message):

    app.logger.debug("'messagedist' command detected", message)

    try:
        message_dist = lookup_message_dist(message.chat.id)
    except ValueError:
        bot.reply_to(message, 'Internal server error')
    else:
        bot.reply_to(message, message_dist)

@bot.message_handler(commands=['yelkomputer'])
def yelkomputer(message):
    app.logger.debug("'yelkomputer' command detected")

    try:
        yelkomputer = lookup_yelkomputer(message.text)
    except ValueError as e:
        bot.reply_to(message, 'Command /yelkomputer doesn\'t need any arguments')
    else:
        bot.reply_to(message, yelkomputer)


# bot.remove_webhook()
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         app.logger.debug(type(e).__name__, e.args)
#         import time
#         time.sleep(5)
