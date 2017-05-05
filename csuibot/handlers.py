from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, lookup_wiki


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


@bot.message_handler(commands=['wiki'])
def wiki(message):
    app.logger.debug("'wiki' command detected")
    term = " ".join(message.text.split()[1:])

    try:
        wiki_summary = lookup_wiki(term)
    except ValueError:
        bot.reply_to(message, 'Command /wiki need an argument')
    except IndexError:
        bot.reply_to(
            message,
            'Page id "' + term + '" does not match any pages. Try another id!'
        )
    else:
        bot.reply_to(message, wiki_summary)


# bot.remove_webhook()
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         app.logger.debug(type(e).__name__, e.args)
#         import time
#         time.sleep(5)
