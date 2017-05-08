import requests
import re
from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, check_palindrome,
                    call_lorem_ipsum, lookup_yelkomputer, get_public_ip,
                    convert_hex2rgb, fetch_latest_xkcd, make_hipster,
                    get_meme, generate_password)
from requests.exceptions import ConnectionError


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


@bot.message_handler(regexp=r'^/password$')
def password_16(message):
    app.logger.debug("'password' command detected")
    app.logger.debug("requested length is 16")
    password_helper(message, 16)


@bot.message_handler(regexp=r'^/password')
def password(message):
    app.logger.debug("'password' command detected")
    length = message.text[10:]
    app.logger.debug("requested length is {}".format(length))
    password_helper(message, length)


def password_helper(message, length):
    try:
        length = int(length)
        password = generate_password(length)
    except TypeError:
        bot.reply_to(message, 'Only a single integer, 1-128, is allowed as length')
    except ValueError:
        bot.reply_to(message, 'Only a single integer, 1-128, is allowed as length')
    except ConnectionError:
        bot.reply_to(
            message,
            'Error connecting to password generator API, please try again later')
    else:
        bot.reply_to(message, password)


@bot.message_handler(regexp=r'^/bot ip')
def ip(message):
    app.logger.debug("'bot' command detected")
    try:
        public_ip = get_public_ip()
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to ipify.org API, please try again later.')
    else:
        bot.reply_to(message, public_ip)


@bot.message_handler(regexp=r'^/hipsteripsum [0-9]{1,3}$')
def hipsteripsum(message):
    app.logger.debug("'hipsteripsum' command detected")
    _, paras_str = message.text.split(' ')
    hipster = make_hipster(int(paras_str))
    bot.reply_to(message, hipster)


@bot.message_handler(regexp=r'^/meme \S{1,} \S{1,}$')
def meme(message):
    app.logger.debug("'meme' command detected")
    _, top, bottom = message.text.split(' ')
    app.logger.debug('top = {}, bottom = {}'.format(top, bottom))

    try:
        meme = get_meme(top, bottom)
    except ValueError:
        bot.reply_to(message, 'Input is invalid')
    else:
        bot.reply_to(message, meme)


@bot.message_handler(regexp=r'^/colou?r (.*)$')
def colour(message):
    app.logger.debug("'colour' command detected")

    try:
        _, hex_str = message.text.split(' ')
        # If hex_str is not the correct format
        if re.match(r'^#[\dA-Fa-f]{6}$', hex_str) is None:
            raise ValueError
        app.logger.debug('hex = {}'.format(hex_str))
        rgb = convert_hex2rgb(hex_str)
    except ValueError:
        bot.reply_to(message, 'Invalid command. '
                              'Please use either /color #HEXSTR or /colour #HEXSTR')
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, 'A connection error occured. Please try again in a moment.')
    except requests.exceptions.HTTPError:
        bot.reply_to(message, 'An HTTP error occured. Please try again in a moment.')
    except requests.exceptions.RequestException:
        bot.reply_to(message, 'An error occured. Please try again in a moment.')
    else:
        bot.reply_to(message, rgb)


def parse_date(text):
    return tuple(map(int, text.split('-')))


@bot.message_handler(regexp=r'^/is_palindrome (.*)$')
def is_palindrome(message):
    app.logger.debug("'is_palindrome' command detected")
    try:
        palindrome = check_palindrome(message)
    except ValueError:
        bot.reply_to(message, 'You can only submit a word')
    else:
        bot.reply_to(message, palindrome)


@bot.message_handler(regexp=r'^/loremipsum$')
def loremipsum(message):
    app.logger.debug("'loremipsum' command detected")
    try:
        loripsum = call_lorem_ipsum()
    except ConnectionError:
        bot.reply_to(message, 'Cannot connect to loripsum.net API')
    else:
        bot.reply_to(message, loripsum)


@bot.message_handler(regexp=r'^/xkcd$')
def xkcd(message):
    app.logger.debug("'xkcd' command detected")
    try:
        comic = fetch_latest_xkcd()
    except ValueError:
        bot.reply_to(message, 'Command is invalid. You can only use "/xkcd" command.')
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, 'A connection error occured. Please try again in a moment.')
    except requests.exceptions.HTTPError:
        bot.reply_to(message, 'An HTTP error occured. Please try again in a moment.')
    except requests.exceptions.RequestException:
        bot.reply_to(message, 'An error occured. Please try again in a moment.')
    else:
        bot.reply_to(message, comic)


@bot.message_handler(commands=['yelkomputer'])
def yelkomputer(message):
    app.logger.debug("'yelkomputer' command detected")

    try:
        yelkomputer = lookup_yelkomputer(message.text)
    except ValueError:
        bot.reply_to(message, 'Command /yelkomputer doesn\'t need any arguments')
    else:
        bot.reply_to(message, yelkomputer)
