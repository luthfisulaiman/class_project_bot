import requests
import re
from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, check_palindrome,
                    call_lorem_ipsum, lookup_yelkomputer, get_public_ip,
                    convert_hex2rgb, fetch_latest_xkcd, make_hipster,
                    get_meme, generate_password, generate_custom_chuck_joke,
                    lookup_define, lookup_kelaskata, call_composer, calculate_binary,
                    remind_me, lookup_isUpWeb, takeSceleNotif, checkTopTropical,
                    getTopManga, getTopMangaMonthly)
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


@bot.message_handler(regexp=r'^/sceleNotif$')
def sceleNoticeHandler(message):
    app.logger.debug("scele command detected")
    try:
        notification = takeSceleNotif()
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to Scele , please try again later.')
    except Exception as e:
        bot.reply_to(message, 'Unexpected Error catched')
    else:
        bot.reply_to(message, notification)


@bot.message_handler(regexp=r'^/checktropical.+$')
def tropicalArtistHandler(message):
    app.logger.debug("top tropical command detected")
    artist = message.text.replace("/checktropical ", "")
    try:
        notification = checkTopTropical(artist)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to Billboard , please try again later.')
    except Exception as e:
        bot.reply_to(message, 'Unexpected Error catched')
    else:
        bot.reply_to(message, notification)


@bot.message_handler(regexp=r'^/topMangaOricon \d{4}\-\d{2}\-\d{2}$')
def oriconMangaHandler(message):
    app.logger.debug("oricon command detected")
    _, date_str = message.text.split(' ')
    year, month, day = parse_date(date_str)
    app.logger.debug(str(year) + " " + str(month) + " " + str(day))
    try:
        notification = getTopManga(year, month, day)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to oricon website , please try again later.')
    except Exception as e:
        bot.reply_to(message, 'Unexpected Error catched')
    else:
        bot.reply_to(message, notification)


@bot.message_handler(regexp=r'^/topMangaOricon \d{4}\-\d{2}$')
def oriconMangaMonthlyHandler(message):
    app.logger.debug("oricon Monthly command detected")
    _, date_str = message.text.split(' ')
    year, month = parse_date(date_str)
    app.logger.debug(str(year) + " === " + str(month))
    try:
        notification = getTopMangaMonthly(year, month)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to oricon website , please try again later.')
    except Exception as e:
        bot.reply_to(message, 'Unexpected Error catched')
    else:
        bot.reply_to(message, notification)


@bot.message_handler(regexp=r'^/chuck ')
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


@bot.message_handler(regexp=r'^\/is_up (.*)$')
def isUp(message):
    app.logger.debug("'is_up' command detected")
    _, url = message.text.split(' ')
    try:
        app.logger.debug('check {} for up/down....')
        result = lookup_isUpWeb(url)
    except ValueError:
        bot.reply_to(message, 'Url is invalid,insert a valid url!.Ex: https://www.google.com')
    else:
        bot.reply_to(message, result)


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


@bot.message_handler(regexp=r'^\/compute ([^01]+(.*)[^01]+)$')
def compute_not_binary(message):
    bot.reply_to(message, 'Not a binary number, Please only input binary number on both sides')


@bot.message_handler(regexp=r'^\/compute help$')
def compute_help(message):
    bot.reply_to(message, '''Binary Calculator v2.0, use /compute <binary><operand><binary>
to start a calculation.''')


@bot.message_handler(regexp=r'^\/compute ([01]+(.*)[01]+)$')
def compute(message):
    app.logger.debug("'compute' command detected")
    _, calculate_str = message.text.split(' ')
    try:
        if '+' in calculate_str:
            binA, binB = calculate_str.split('+')
            op = '+'
        elif '-' in calculate_str:
            binA, binB = calculate_str.split('-')
            op = '-'
        elif '*' in calculate_str:
            binA, binB = calculate_str.split('*')
            op = '*'
        elif '/' in calculate_str:
            binA, binB = calculate_str.split('/')
            op = '/'
        else:
            raise ValueError
    except ValueError:
        bot.reply_to(message, "Operator is invalid, please use '+', '-', '*', or '/'")
    else:
        result = calculate_binary(binA, op, binB)
        bot.reply_to(message, result)


@bot.message_handler(regexp=r'^/define (.*)$')
def define(message):
    app.logger.debug("'define' command detected")
    command = " ".join(message.text.split()[1:])

    try:
        define_ = lookup_define(command)
    except requests.HTTPError as e:
        bot.reply_to(
            message,
            '"'+command + '" is not an english word')
    except ValueError as e:
        bot.reply_to(message, 'Command /define need an argument')
    else:
        bot.reply_to(message, define_)


@bot.message_handler(regexp=r'^/kelaskata (.*)$')
def kelaskata(message):
    app.logger.debug("'kelaskata' command detected")
    command = " ".join(message.text.split()[1:])

    try:
        kelas_kata = lookup_kelaskata(command)
    except ValueError as e:
        bot.reply_to(message, 'Try /kelaskata [word]')
    except requests.ConnectionError as e:
        bot.reply_to(
            message,
            '"'+command + '" is not a word')
    else:
        bot.reply_to(message, kelas_kata)


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


@bot.message_handler(regexp=r'^\/sound_composer \w+$')
def composer(message):
    app.logger.debug("'sound_composer' command detected")
    _, username = message.text.split(' ')
    app.logger.debug('username = {}'.format(username))

    try:
        track = call_composer(username)
    # except ValueError: cannot try fetching from SoundCloud API
    #     bot.reply_to(message, 'Username not found')
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to Soundcloud API')
    else:
        bot.reply_to(message, track)
