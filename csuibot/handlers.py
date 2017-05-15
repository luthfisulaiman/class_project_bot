from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, get_oricon_books,
                    generate_custom_chuck_joke, lookup_yelkomputer)


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


@bot.message_handler(regexp=r'^/chuck')
def custom_chuck_joke(message):
    app.logger.debug("'chuck' command detected")
    try:
        _, first_name, last_name = message.text.split(' ')
        app.logger.debug("first = {}, last = {}".format(first_name, last_name))
        joke = generate_custom_chuck_joke(first_name, last_name)
    except ValueError:
        bot.reply_to(message,
                     'Only two words, first name and last name, are accepted as input.')
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to icndb.com API, please try again later.')
    else:
        bot.reply_to(message, joke)


def parse_date(text):
    return tuple(map(int, text.split('-')))


@bot.message_handler(regexp=r'^/oricon books ')
def oricon_books(message):
    app.logger.debug("'oricon' command detected")
    app.logger.debug("oricon command type is 'books'")

    try:
        _, _, weekly, request_date = message.text.split(' ')
        if (weekly != 'weekly'):
            top10 = 'Oricon books command currently only supports '\
                    'weekly ratings at this time.'
        else:
            app.logger.debug("oricon command type is 'weekly'")
            top10 = get_oricon_books(request_date)
    except ValueError:
        error = "Invalid command structure. Example: " \
                "'/oricon books weekly 2017-05-01'"
        bot.reply_to(message, error)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to the oricon.co.jp website.')
    else:
        bot.reply_to(message, top10)


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
