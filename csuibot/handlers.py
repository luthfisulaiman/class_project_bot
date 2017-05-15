import requests
import re
from . import app, bot
from .utils import (lookup_zodiac, lookup_chinese_zodiac, check_palindrome,
                    call_lorem_ipsum, lookup_yelkomputer, get_public_ip,
                    convert_hex2rgb, fetch_latest_xkcd, make_hipster,
                    get_meme, generate_password, get_chuck, generate_custom_chuck_joke,
                    lookup_define, lookup_kelaskata, call_composer, calculate_binary,
                    remind_me, lookup_isUpWeb, takeSceleNotif, lookup_definisi,
                    manage_notes, lookup_dayofdate, compute, call_discrete_material,
                    lookup_message_dist, add_message_dist,
                    lookup_marsfasilkom, lookup_yelfasilkom, data_processor, get_top_poster)
from requests.exceptions import ConnectionError
import datetime


def message_decorator(func):
    def wrapper(message):
        now = datetime.datetime.now()
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
        'CSUIBot v0.0.3\n\n'
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


@bot.message_handler(regexp=r'^/triviaplant$')
def plant_trivia(message):
    try:
        txt = message.text
        msg = data_processor.fetch_user_input(txt)
    except ValueError:
        bot.reply_to(message, 'input is invalid')
    else:
        bot.reply_to(message, msg)


@bot.message_handler(regexp=r'^/askplant (.*)$')
def plant_ask(message):
    try:
        txt = message.text
        msg = data_processor.fetch_user_input(txt)
    except ValueError:
        bot.reply_to(message, 'input is invalid')
    else:
        bot.reply_to(message, msg)


@bot.message_handler(regexp=r'^/topposters$')
def top_poster(message):
    app.logger.debug("'/topposter' command detected")
    try:
        msg = get_top_poster()
    except ValueError:
        bot.reply_to(message, 'input is invalid')
    else:
        bot.reply_to(message, msg)


@bot.message_handler(commands=['yelfasilkom'])
def yelfasilkom(message):
    app.logger.debug("'yelfasilkom' command detected")

    try:
        yelfasilkom = lookup_yelfasilkom(message.text)
    except ValueError as e:
        bot.reply_to(message, 'Command /yelfasilkom doesn\'t need any arguments')
    else:
        bot.reply_to(message, yelfasilkom)


@bot.message_handler(regexp=r'^/notes .*$')
def note(message):
    app.logger.debug('"notes" command detexted')
    if message.text.find(' ') != -1:
        text = message.text.split(' ', 1)
        reply = ''

        app.logger.debug('input = {}'.format(text[1]))
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


@bot.message_handler(regexp=r'^/definisi [A-Za-z0-9 -]+$')
def definisi(message):
    if message.text.find(' ') != -1:
        app.logger.debug("'definisi' command detected")
        _, word_str = message.text.split(' ', 1)

        app.logger.debug('input : {}'.format(word_str))
        try:
            meaning = lookup_definisi(word_str)
        except requests.ConnectionError:
            bot.reply_to(message, 'Oops! There was a problem. Maybe try again later :(')
        else:
            bot.reply_to(message, meaning)
    else:
        app.logger.debug("'definisi_help' command detected")
        bot.reply_to(message, '/definisi [word] : return definition of' +
                              ' the word in indonesian language\n')


@bot.message_handler(regexp=r'^/sceleNotif$')
def sceleNoticeHandler(message):
    app.logger.debug("scele command detected")
    try:
        notification = takeSceleNotif()
    except Exception as e:
        bot.reply_to(message, 'Error catched')
    else:
        bot.reply_to(message, notification)


@bot.message_handler(regexp=r'^/chuck$')
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


@bot.message_handler(regexp=r'^/dayofdate \d{4}\-\d{2}\-\d{2}$')
def dayofdate(message):
    app.logger.debug("'dayofdate' command detected")
    _, date_str = message.text.split(' ')
    year, month, day = parse_date(date_str)
    app.logger.debug('year = {}, month = {}, day = {}'.format(year, month, day))

    try:
        datetime.datetime(year, month, day)
        # if (newDate):
        # check invalid date such as leap year, month 13 etc
        dayofdate = lookup_dayofdate(year, month, day)
    except ValueError:
        bot.reply_to(message,
                     'Incorrect use of dayofdate command. '
                     'Please write a valid date in the form of yyyy-mm-dd, '
                     'such as 2016-05-13')
    else:
        bot.reply_to(message, dayofdate)


# empty dayofdate args
@bot.message_handler(regexp=r'^/dayofdate$')
def empty_dayofdate(message):
    app.logger.debug("invalid 'dayofdate' command detected")
    bot.reply_to(message,
                 'Incorrect use of dayofdate command. '
                 'Please write a valid date in the form of yyyy-mm-dd, '
                 'such as 2016-05-13')


# invalid dayofdate calls
@bot.message_handler(regexp=r'^/dayofdate (?!\d{4}\-\d{2}\-\d{2}).*$')
def invalid_dayofdate(message):
    app.logger.debug("invalid 'dayofdate' command detected")
    bot.reply_to(message,
                 'Incorrect use of dayofdate command. '
                 'Please write a valid date in the form of yyyy-mm-dd, '
                 'such as 2016-05-13')


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


@bot.message_handler(regexp=r'^\/tellme .+$')
def get_discrete_material(message):
    app.logger.debug("tellme detected")
    query = message.text.replace('/tellme ', '')
    query = query.lower()
    app.logger.debug('searching for {} in discretematerial'.format(query))
    try:
        result = call_discrete_material(query)
    except ValueError:
        bot.reply_to(message, "Invalid Value")
    else:
        bot.reply_to(message, result)


@bot.message_handler(regexp=r'^/compute ([0-9]+[\/\+\-\*][0-9]+)*$')
def calculate(message):
    try:
        result = compute(message)
    except NameError:
        bot.reply_to(message, 'Invalid command, please enter only numbers and operators')
    except ZeroDivisionError:
        bot.reply_to(message, 'Cannot divide by zero')
    else:
        bot.reply_to(message, result)


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
def compute_binary(message):
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


@bot.message_handler(commands=['marsfasilkom'])
def marsfasilkom(message):
    app.logger.debug("'marsfasilkom' command detected")

    try:
        marsfasilkom = lookup_marsfasilkom(message.text)
    except ValueError:
        bot.reply_to(message, 'Command /marsfasilkom doesn\'t need any arguments')
    else:
        bot.reply_to(message, marsfasilkom)
