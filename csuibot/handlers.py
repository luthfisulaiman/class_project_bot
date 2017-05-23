from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, get_nearest_hangout
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


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


@bot.message_handler(regexp=r'^/hangout_kuy$')
def hangout_nearby(message):

    app.logger.debug("'hangout_kuy' command detected")
    str_msg = 'Tap to get your location and get nearby hangout place!'

    k_array = []
    keyboard = KeyboardButton('Go!', request_location=True)
    k_array.append(keyboard)

    reply_keyboard = ReplyKeyboardMarkup()
    reply_keyboard.add(keyboard)

    bot.send_message(chat_id=message.chat.id, text=str_msg, reply_markup=reply_keyboard)


@bot.message_handler(content_types=['location'])
def get_location(message):
    loc = dict(latitude=message.location.latitude, longitude=message.location.longitude)

    try:
        res = get_nearest_hangout(loc['longitude'], loc['latitude'])
    except ValueError:
        bot.reply_to(message, 'input is invalid')
    else:
        bot.send_photo(message.chat.id, res['nearest'].image_dir)
        bot.reply_to(message, res['message'])


def parse_date(text):
    return tuple(map(int, text.split('-')))
