from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, remind_me


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


@bot.message_handler(commands=['chuck'])
def chuck(message):
    app.logger.debug("'chuck' command detected")
    try:
        joke = get_chuck(message.text)
    except ConnectionError:
        bot.reply_to(message, 'Chuck Norris doesn\'t need internet connection'
                              ' to connect to ICNDb API, too bad you\'re not him')
    except ValueError:
        bot.reply_to(message, 'Command /chuck doesn\'t need any arguments')
    else:
        bot.reply_to(message, joke)


def parse_date(text):
    return tuple(map(int, text.split('-')))


@bot.message_handler(regexp=r'^\/remindme (\d+) (.*)$')
def remind(message):
    app.logger.debug("'remindme' command detected")
    time_str = message.text.split(' ')
    i = 2
    text = ""
    while (i < len(time_str)):
        if(i == (len(time_str)-1)):
            text += time_str[i]
        else:
            text += time_str[i] + " "
        i += 1
    try:
        bot.reply_to(message, "You have a new reminder in " + time_str[1] + " second")
        app.logger.debug(time_str[1])
        reply_text = remind_me(time_str[1], text)
        app.logger.debug(time_str[1])
    except ValueError:
        bot.reply_to(message, "Invalid time input, only positive integer accepted.")
    except Exception:
        bot.reply_to(message, "Please input from range 0-29 only")
    else:
        bot.reply_to(message, reply_text)