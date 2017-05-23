from . import app, bot
import requests
import re
import os
import urllib
from .utils import (lookup_zodiac, lookup_chinese_zodiac, check_palindrome,
                    call_lorem_ipsum, lookup_yelkomputer, get_public_ip,
                    convert_hex2rgb, fetch_latest_xkcd, make_hipster,
                    get_meme, generate_password, get_chuck, generate_custom_chuck_joke,
                    lookup_define, lookup_kelaskata, call_composer, calculate_binary,
                    remind_me, lookup_isUpWeb, takeSceleNotif, lookup_definisi,
                    manage_notes, lookup_dayofdate, compute, call_discrete_material,
                    define_sound, get_articles,
                    lookup_message_dist, add_message_dist, lookup_wiki, get_comic,
                    lookup_marsfasilkom, lookup_yelfasilkom, data_processor, similar_text,
                    find_hot100_artist, find_newage_artist, find_hotcountry_artist,
                    top_ten_cd_oricon, lookup_top10_billboard_chart,
                    lookup_hotcountry, lookup_newage, get_fake_json, lookup_lang,
                    lookup_billArtist, lookup_weton, get_oricon_books,
                    lookup_url, lookup_artist, extract_colour, checkTopTropical,
                    getTopManga, getTopMangaMonthly, auto_tag, lookup_HotJapan100,
                    get_tweets, get_aqi_city, get_aqi_coord, lookup_sentiment_new,
                    image_is_sfw, get_mediawiki, save_mediawiki_url, generate_schedule,
                    get_available_schedules, get_schedules, lookup_anime, preview_music,
                    airing_check, lookup_airing, fetch_apod, lookup_hospital,
                    lookup_random_hospital, reply_random_hospital,
                    change_cinema, find_movies)
from requests.exceptions import ConnectionError
import datetime
from telebot import types


def message_decorator(func):
    def wrapper(message):
        now = datetime.datetime.now()
        hour = (now.hour + 7) % 24
        chat_id = message.chat.id
        add_message_dist(chat_id, hour)
        return func(message)

    return wrapper


schedules = {}
lookup_anime_property = {}


class EntrySchedule:
    def __init__(self, group):
        self.group = group
        self.date = None
        self.time = None


@bot.message_handler(regexp=r'^/about$')
def help(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'CSUIBot v0.0.3\n\n'
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


@bot.message_handler(commands=['aqi'])
def air_quality(message):
    app.logger.debug("'aqi' command detected")
    arr_loc = message.text.split(' ', 1)

    if(len(arr_loc) > 1 and not arr_loc[1].isspace() and len(arr_loc[1]) > 0):
        loc = arr_loc[1]

        if(re.match(r'^(\d+[.]?\d+|\d) (\d+[.]?\d+|\d)$', loc)):
            try:
                result = get_aqi_coord(loc)
            except ConnectionError:
                bot.reply_to(message, "Unable to connect to aqicn.org, please try again later")
            else:
                bot.reply_to(message, result)

        elif (re.match(r'^[a-zA-Z0-9\s]*$', loc)):
            try:
                result = get_aqi_city(loc)
            except ConnectionError:
                bot.reply_to(message, "Unable to connect to aqicn.org, please try again later")
            else:
                bot.reply_to(message, result)

    else:
        bot.reply_to(message, "Invalid city name or coordinate, please try again")


@bot.message_handler(regexp=r'^/tweet ?.* ?.*$')
def get_notif_twitter(message):
    app.logger.debug("'tweet recent' command detected")
    try:
        _, cmd2, user = message.text.split(' ')
    except ValueError:
        bot.reply_to(message, 'Wrong command')
    else:
        app.logger.debug("option = {}".format(cmd2))
        if cmd2 == 'recent':
            five_tweets = get_tweets(user)
            bot.reply_to(message, five_tweets)
        else:
            bot.reply_to(message, 'Wrong command or invalid user')


@bot.message_handler(regexp=r'^triviaplant')
def plant_trivia(message):
    try:
        txt = message.text
        msg = data_processor.fetch_user_input(txt)
    except ValueError:
        bot.reply_to(message, 'input is invalid')
    else:
        bot.reply_to(message, msg)


@bot.message_handler(regexp=r'^askplant')
def plant_ask(message):
    try:
        txt = message.text
        msg = data_processor.fetch_user_input(txt)
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


@bot.message_handler(regexp=r'^/oricon comic \d{4}\-\d{2}\-\d{2}$')
def oriconMangaHandler(message):
    app.logger.debug("oricon command detected")
    _, _, date_str = message.text.split(' ')
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


@bot.message_handler(regexp=r'^/oricon comic \d{4}\-\d{2}$')
def oriconMangaMonthlyHandler(message):
    app.logger.debug("oricon Monthly command detected")
    _, _, date_str = message.text.split(' ')
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


@bot.message_handler(func=lambda message: message.chat.type == "group", regexp="jadwal")
def jadwal(message):
    app.logger.debug("'jadwal' command detected")
    future_schedules = get_schedules(message.chat.id)
    if len(future_schedules) > 0:
        for schedule in future_schedules:
            bot.send_message(message.chat.id, schedule)
    else:
        bot.send_message(message.chat.id, 'No future schedules are found.')


@bot.message_handler(commands=['create_schedule'],
                     func=lambda message: message.chat.type == "group")
def create_schedule(message):
    app.logger.debug("'create_schedule' command detected")
    entry = EntrySchedule(message.chat.id)
    schedules[message.from_user.id] = entry
    msg = bot.send_message(message.from_user.id, 'When should the schedule be created?')
    bot.register_next_step_handler(msg, date_schedule)


def date_schedule(date_message):
    app.logger.debug("date of schedule step started")
    if date_message.text == '/cancel':
        schedules.pop(date_message.from_user.id)
        bot.reply_to(date_message, 'create_schedule canceled.')
        return

    try:
        y, m, d = parse_date(date_message.text)
        if datetime.date(y, m, d) >= datetime.datetime.now().date():
            entry = schedules[date_message.from_user.id]

            avl_hours = get_available_schedules(entry.group, date_message.text)
            avl_hours.sort()
            if len(avl_hours) <= 0:
                error_text = "That date's full. Try another date or use /cancel to cancel."
                msg = bot.reply_to(date_message, error_text)
                bot.register_next_step_handler(msg, date_schedule)
                return

            app.logger.debug("date of schedule is {}".format(date_message.text))
            entry.date = date_message.text
            markup = types.ReplyKeyboardMarkup()
            for avl_hour in avl_hours:
                markup.add(types.KeyboardButton("{}.00".format(avl_hour)))
            msg = bot.send_message(date_message.from_user.id,
                                   'Here are the available hours for {}.'.format(
                                        date_message.text),
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, time_schedule)
        else:
            msg = bot.reply_to(date_message,
                               'You cannot make a schedule for the past. Try again.')
            bot.register_next_step_handler(msg, date_schedule)
    except ValueError:
        msg = bot.reply_to(date_message, 'The requested date is invalid. Try again.')
        bot.register_next_step_handler(msg, date_schedule)


def time_schedule(time_message):
    app.logger.debug("time of schedule started")
    if time_message.text == '/cancel':
        schedules.pop(time_message.from_user.id)
        bot.reply_to(time_message, 'create_schedule canceled.')
        return

    app.logger.debug("time of schedule is {}".format(time_message.text))
    entry = schedules[time_message.from_user.id]
    entry.time = time_message.text.split('.')[0]
    msg = bot.reply_to(time_message, 'Give a description for this schedule.',
                       reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, desc_schedule)


def desc_schedule(desc_message):
    app.logger.debug("desc of schedule started")
    if desc_message.text == '/cancel':
        schedules.pop(desc_message.from_user.id)
        bot.reply_to(desc_message, 'create_schedule canceled.')
        return

    app.logger.debug("desc of schedule is {}".format(desc_message.text))
    entry = schedules[desc_message.from_user.id]
    generate_schedule(entry.group, entry.date, entry.time, desc_message.text)
    bot.reply_to(desc_message, 'Schedule created successfully.')
    bot.send_message(entry.group, 'A schedule has been created.')
    bot.send_message(entry.group,
                     "{} jam {}.00: {}".format(entry.date, entry.time, desc_message.text))
    schedules.pop(desc_message.from_user.id)


@bot.message_handler(commands=['sentiment'])
def sentiment_new(message):
    app.logger.debug("'sentiment' command detected")
    text = message.text[11::]
    app.logger.debug('text = {}'.format(text))
    try:
        result = lookup_sentiment_new(text)
    except ValueError:
        bot.reply_to(message, 'Command /sentiment need an argument')
    else:
        bot.reply_to(message, result)


@bot.message_handler(regexp=r'^/soundhelp$')
def soundcliphelp(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'SOUNDCLIPS!\n\n'
        'To use this bot, start with /soundclip\n'
        'followed by a keyword\n\n'
        'Available soundclips:\n'
        '-Goofy\n'
        '-Tom Pain\n'
        '-Tom Scream\n'
        '-Wilhelm\n'
    )
    bot.reply_to(message, about_text)


@bot.message_handler(regexp=r'^/soundclip [a-z A-Z 0-9]*$')
def soundclip(message):
    soundtitle = define_sound(message.text.lower())

    try:
        soundclip = open(soundtitle, 'rb')
    except FileNotFoundError:
        bot.reply_to(message, 'Sound clip not found')
    else:
        bot.send_voice(message.chat.id, soundclip)


@bot.message_handler(regexp=r'^/oricon books ')
def oricon_books(message):
    app.logger.debug("'oricon' command detected")
    app.logger.debug("oricon command type is 'books'")

    try:
        _, _, weekly, request_date = message.text.split(' ')
        if (weekly != 'weekly'):
            top10 = 'Oricon books command currently only supports ' \
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
        if (i == (len(time_str) - 1)):
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
            '"' + command + '" is not an english word')
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
            '"' + command + '" is not a word')
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


@bot.message_handler(regexp=r'^/xkcd')
def xkcd(message):
    app.logger.debug("'xkcd' command detected")
    command = message.text.split(" ")
    if (len(command) == 1):
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
    elif (len(command) == 2):
        try:
            comic = get_comic(command[1])
        except requests.exceptions.ConnectionError:
            bot.reply_to(message, 'Can\'t connect to the server. Please try again later')
        else:
            bot.reply_to(message, comic)
    else:
        bot.reply_to(message, 'Command is invalid. please user /xkcd <id> or /xkcd format')


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


@bot.message_handler(regexp=r'/is_sfw( .*)?')
def check_sfw_command(message):
    app.logger.debug("invalid is_sfw command detected")

    bot.reply_to(message, 'to use is_sfw command, send photo caption with /is_sfw')


def is_caption_image(message):
    sfw_captions = ['/is_sfw']
    return message.caption in sfw_captions


@bot.message_handler(func=is_caption_image, content_types=['photo'])
def check_sfw_image(message):
    app.logger.debug("'is_sfw' command detected with photo sent")

    photo_file_path = bot.get_file(message.photo[1].file_id).file_path
    app.logger.debug(photo_file_path)
    sfw_check = image_is_sfw(photo_file_path)
    bot.reply_to(message, sfw_check)


@bot.message_handler(regexp=r'^/getnews [a-z A-Z 0-9]*$')
def news(message):
    app.logger.debug("'get news' command detected")
    command, keyword = message.text.split(' ', 1)

    try:
        news = get_articles(message.text)['value']
    except ConnectionError:
        bot.reply_to(message, "Sorry, connection error. Try again later insyaAllah bisa")
    else:
        bot.reply_to(message, news)


@bot.message_handler(regexp=r'^/billboard japan100$')
def japan100(message):
    rss_url = "http://www.billboard.com/rss/charts/japan-hot-100"
    html = urllib.request.urlopen(rss_url).read()
    html = str(html)
    try:
        reply = lookup_HotJapan100(html)
    except ConnectionError:
        bot.reply_to(message, '''The connection error
Please try again in a few minutes''')
    else:
        bot.reply_to(message, reply)


@bot.message_handler(regexp=r'^\/youtube\s*$')
def youtube_no_url(message):
    bot.reply_to(message, "'youtube' command needs an url")


@bot.message_handler(regexp=r'^(\/youtube) .+$')
def youtube(message):
    app.logger.debug("'youtube' command detected")
    _, url = message.text.split(' ')

    try:
        youtube = lookup_url(url)
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to Youtube')
    else:
        bot.reply_to(message, youtube)


@bot.message_handler(regexp=r'^(\/billboard japan100) .+$')
def japanartist(message):
    app.logger.debug("'billboard japan100 artist comand detacted'")
    artist = " ".join(message.text.split(' ')[2:])
    app.logger.debug('artist = {}'.format(artist))

    try:
        _artist = lookup_artist(artist)
    # except ValueError:
    #     bot.reply_to(message, 'Command /billboard japan100 need an arguments')
    except ConnectionError:
        bot.reply_to(message, 'Error connecting to Billboard RSS Feed')
    else:
        bot.reply_to(message, _artist)


@bot.message_handler(commands=['detect_lang'])
def detect_lang(message):
    app.logger.debug("'detect_lang' command detected")
    arg = " ".join(message.text.split()[1:])

    try:
        used_langs = lookup_lang(arg)
    except ValueError as e:
        bot.reply_to(message, str(e))
    except LookupError as e:
        bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, used_langs)


@bot.message_handler(commands=['fake_json'])
def fake_json(message):
    app.logger.debug("'fake_json' command detected")

    arg = " ".join(message.text.split()[1:])
    try:
        fakejson = get_fake_json(arg)
    except ValueError as e:
        bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, fakejson)


@bot.message_handler(regexp=r'^\/docs_sim')
def similar(message):
    app.logger.debug("'similarity text' command detected")
    command = message.text.split(' ')
    if (len(command) != 3):
        bot.reply_to(message, 'Command invalid, please use /docs_sim <text1> <text2> format')
    else:
        try:
            percentage = similar_text(command[1], command[2])
        except requests.exceptions.HTTPError:
            bot.reply_to(message, 'HTTP Error occurs, please try again later')
        else:
            bot.reply_to(message, percentage)


@bot.message_handler(regexp=r'/billboard (tropical|hot100|200)$')
def billboard_chart(message):
    app.logger.debug("billboard command detected")
    _, chart_category = message.text.split(' ')
    app.logger.debug('chart category = {}'.format(str(chart_category)))
    result = lookup_top10_billboard_chart(chart_category)
    bot.reply_to(message, result)


@bot.message_handler(regexp=r'/oricon jpsingles(| .*)$')
def oricon_cd(message):
    app.logger.debug("'oricon CD' command detected")
    help_text = 'Usage: /oricon jpsingles [weekly|daily]' + \
                ' YYYY[-MM[-DD]]\nNote: for weekly chart you must insert' + \
                ' date of the monday in that week'

    command = message.text.split(' ')
    app.logger.debug(command)

    if len(command) == 3:
        if len(command[2].split('-')) == 1:
            chart_type = 'y'
        else:
            chart_type = 'm'

        chart = top_ten_cd_oricon(chart_type, command[2])
        bot.reply_to(message, chart)
    elif len(command) == 4:
        if command[2] == 'weekly':
            chart_type = 'w'
        elif command[2] == 'daily':
            chart_type = 'd'
        else:
            bot.reply_to(message, help_text)
            return
        chart = top_ten_cd_oricon(chart_type, command[3])
        bot.reply_to(message, chart)
    else:
        bot.reply_to(message, help_text)


@bot.message_handler(regexp=r'^/billboard hot100 .*$')
def hot100_artist(message):
    app.logger.debug("'billboard hot100' command detected")

    s2 = "hot100 "

    name = (message.text[message.text.index(s2) + len(s2):])

    app.logger.debug("'billboard hot100' argument is " + name)
    try:
        artist = find_hot100_artist(name)
    except ConnectionError:
        bot.reply_to(message, "Connection Error")
    else:
        bot.reply_to(message, artist)


@bot.message_handler(regexp=r'^/billboard newage .*$')
def newage_artist(message):
    app.logger.debug("'billboard newage' command detected")

    s2 = "newage "

    name = (message.text[message.text.index(s2) + len(s2):])

    app.logger.debug("'billboard newage' argument is " + name)
    try:
        artist = find_newage_artist(name)
    except ConnectionError:
        bot.reply_to(message, "Connection Error")
    else:
        bot.reply_to(message, artist)


@bot.message_handler(regexp=r'^/billboard hotcountry .*$')
def hotcountry_artist(message):
    app.logger.debug("'billboard hotcountry' command detected")

    s2 = "hotcountry "

    name = (message.text[message.text.index(s2) + len(s2):])

    app.logger.debug("'billboard hotcountry' argument is " + name)
    try:
        artist = find_hotcountry_artist(name)
    except ConnectionError:
        bot.reply_to(message, "Connection Error")
    else:
        bot.reply_to(message, artist)


@bot.message_handler(regexp=r'^/billboard hotcountry$')
def hotcountry(message):
    app.logger.debug("'billboard' command detected")
    try:
        hotcountry = lookup_hotcountry()
    except ConnectionError:
        bot.reply_to(message, 'Cannot connect to billboard API')
    else:
        bot.reply_to(message, hotcountry)


@bot.message_handler(regexp=r'^/billboard newage$')
def newage(message):
    app.logger.debug("'billboard' command detected")
    try:
        newage = lookup_newage()
    except ConnectionError:
        bot.reply_to(message, 'Cannot connect to billboard API')
    else:
        bot.reply_to(message, newage)


@bot.message_handler(regexp=r'^/billboard bill200 (.*)$')
def billArtist(message):
    app.logger.debug("'billboard' command detected")
    try:
        name = message.text[message.text.index("bill200") + len("bill200") + 1:]
        billArtist = lookup_billArtist(name)
        app.logger.debug("artist's name" + name)
        app.logger.debug("lookup result" + billArtist)
    except ConnectionError:
        bot.reply_to(message, 'Cannot connect to billboard API')
    else:
        bot.reply_to(message, billArtist)


@bot.message_handler(regexp=r'^/primbon \d{4}\-\d{2}\-\d{2}$')
@message_decorator
def primbon(message):
    app.logger.debug("'primbon' command detected")
    _, date_str = message.text.split(' ')
    year, month, day = parse_date(date_str)

    weton = lookup_weton(year, month, day)
    bot.reply_to(message, weton)


def check_caption_colour(message):
    return message.caption in ['/bgcolour', '/fgcolour']


@bot.message_handler(content_types=['photo'], func=check_caption_colour)
def extract_colour_from_image(message):
    app.logger.debug("'extract_colour_from_image' handler executed")
    try:
        extracted = extract_colour(message)
    except IndexError:
        bot.reply_to(message, 'Colour not extracted.')
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, 'A connection error occured. Please try again in a moment.')
    except requests.exceptions.HTTPError:
        bot.reply_to(message, 'An HTTP error occured. Please try again in a moment.')
    except requests.exceptions.RequestException:
        bot.reply_to(message, 'An error occured. Please try again in a moment.')
    else:
        bot.reply_to(message, extracted)


def check_caption_tag(message):
    return message.caption in ['/tag']


@bot.message_handler(content_types=['photo'], func=check_caption_tag)
def tagimage(message):
    app.logger.debug("'tag image' command detected")
    try:
        tag = auto_tag(message)
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to Immaga API")
    except requests.exceptions.HTTPError:
        bot.reply_to(message, "HTTP Error")
    else:
        bot.reply_to(message, tag)


@bot.message_handler(regexp=r'^/cgv_gold_class$')
def cgv_gold(message):
    app.logger.debug("'cgv_gold_class' command detected")
    try:
        gold = find_movies(message.text)
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to CGV Blitz")
    else:
        bot.reply_to(message, gold)


@bot.message_handler(regexp=r'^/cgv_regular_2d$')
def cgv_reg(message):
    app.logger.debug("'cgv_regular' command detected")
    try:
        twod = find_movies(message.text)
    except ConnectionError:
        bot.reply_to(message, "Cannoct connect to CGV Blitz")
    else:
        bot.reply_to(message, twod)


@bot.message_handler(regexp=r'^/cgv_4dx_3d_cinema$')
def cgv_3dcinema(message):
    app.logger.debug("'cgv_4dx_3d_cinema' command detected")
    try:
        threed = find_movies(message.text)
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to CGV Blitz")
    else:
        bot.reply_to(message, threed)


@bot.message_handler(regexp=r'^/cgv_velvet$')
def cgv_velvet(message):
    app.logger.debug("'cgv_velvet' command detected")
    try:
        velvet = find_movies(message.text)
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to CGV Blitz")
    else:
        bot.reply_to(message, velvet)


@bot.message_handler(regexp=r'^/cgv_sweet_box$')
def cgv_sweetbox(message):
    app.logger.debug("'cgv_sweet_box' command detected")
    try:
        sweetbox = find_movies(message.text)
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to CGV Blitz")
    else:
        bot.reply_to(message, sweetbox)


@bot.message_handler(regexp=r'^/cgv_change_cinema ?.*$')
def cgv_change(message):
    app.logger.debug("'cgv_change_cinema' command detected")
    cmd1, url = message.text.split(' ')

    app.logger.debug("url is {}".format(url))
    try:
        if cmd1 == '/cgv_change_cinema':
            changed = change_cinema(url)
        else:
            raise Exception
    except ConnectionError:
        bot.reply_to(message, "Cannot connect to CGV Blitz")
    except Exception:
        bot.reply_to(message, "Wrong command")
    else:
        bot.reply_to(message, changed)


@bot.message_handler(regexp=r'^/is_airing')
def airing(message):
    if message.chat.type == "private":
        app.logger.debug("'airing anime' command detected")
        command = message.text.split(" ")
        if len(command) == 2:
            words = list(command[1])
            anime = ""
            for word in words:
                if(word == "_"):
                    anime += " "
                else:
                    anime += word
            try:
                res = airing_check(anime)
            except requests.exceptions.HTTPError:
                bot.reply_to(message, 'HTTP error occurs, please try again in a minute')
            except ConnectionError:
                bot.reply_to(message, 'Connection error occurs, please try again in a minute')
            else:
                bot.reply_to(message, res)
        else:
            output = ('Command invalid, please use /is_airing <anime>'
                      'format and replace space in <anime> with underscore (_)')
            bot.reply_to(message, output)


@bot.message_handler(regexp=r'hari ini nonton apa?')
def lookup_today(message):
    if message.chat.type == "group":
        app.logger.debug("'lookup anime today' command detected")
        try:
            res = lookup_airing()
        except requests.exceptions.HTTPError:
            bot.reply_to(message, 'HTTP error occurs, please try again in a minute')
        except ConnectionError:
            bot.reply_to(message, 'Connection error occurs, please try again in a minute')
        else:
            bot.reply_to(message, res)


@bot.message_handler(regexp=r'^/lookup_anime')
def lookup_anime_livechart(message):
    app.logger.debug("'lookup_anime' command detected.")
    markup = types.ReplyKeyboardMarkup()
    lookup_anime_property[message.from_user.id] = {}
    try:
        for year in range(2001, 2017):
            markup.add(types.KeyboardButton('{}'.format(str(year))))
        msg = bot.send_message(message.from_user.id, 'Choose year', reply_markup=markup)
        bot.register_next_step_handler(msg, lookup_anime_season)
    except ConnectionError as e:
        bot.reply_to(message, str(e))


def lookup_anime_season(message):
    app.logger.debug("'lookup_anime' Choose season")
    year = message.text
    lookup_anime_property[message.from_user.id]['year'] = year
    seasons = ['spring', 'fall', 'summer', 'winter']
    markup = types.ReplyKeyboardMarkup()
    for s in seasons:
        markup.add(types.KeyboardButton(s))
    try:
        msg = bot.reply_to(message, 'Choose season', reply_markup=markup)
        bot.register_next_step_handler(msg, lookup_anime_genre)
    except ConnectionError as e:
        bot.reply_to(message, str(e))


def lookup_anime_genre(message):
    season = message.text
    lookup_anime_property[message.from_user.id]['season'] = str(season)
    app.logger.debug("'lookup_anime' Type genre")
    try:
        msg = bot.reply_to(message, 'Type genre')
        app.logger.debug('Choosed genre {}'.format(msg.text))
        bot.register_next_step_handler(msg, lookup_anime_list)
    except ConnectionError as e:
        bot.reply_to(message, str(e))


def lookup_anime_list(message):
    try:
        year = lookup_anime_property[message.from_user.id]['year']
        season = lookup_anime_property[message.from_user.id]['season']
        genre = message.text
        app.logger.debug('::: {} {} {} '.format(year, season, genre))
        result = lookup_anime(genre, season, year)
    except ConnectionError as e:
        bot.reply_to(message, 'Request timeout {} '.format(str(e)),
                     reply_markup=types.ReplyKeyboardRemove())
    except Exception:
        bot.reply_to(message, 'cannot find anime that matches with user',
                     reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.reply_to(message, result,
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['add_wiki'])
def add_wiki(message):
    app.logger.debug("'add_wiki' command detected")
    url = " ".join(message.text.split()[1:])
    try:
        result = save_mediawiki_url(url)
    except ValueError as e:
        bot.reply_to(message, str(e))
    except ConnectionError as e:
        bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, result)


@bot.message_handler(commands=['random_wiki_article'])
def random_wiki_article(message):
    app.logger.debug("'random_wiki_article' command detected")
    args = " ".join(message.text.split()[1:])
    try:
        result = get_mediawiki(args)
    except EnvironmentError as e:
        bot.reply_to(message, str(e))
    else:
        if args is '':
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            for title in result:
                keyboard.add(title)
            bot.send_message(message.chat.id, 'Select an article...', reply_markup=keyboard)
        else:
            bot.reply_to(message, result)


@bot.message_handler(regexp=r'^/itunes_preview')
def preview(message):
    app.logger.debug("'itunes preview' command detected")
    command = message.text.split(' ')
    if (len(command) != 2):
        output = ('Command invalid, please use /itunes_preview'
                  ' <artist> format, and seperate word in artist name with _')
        bot.reply_to(message, output)
    else:
        words = list(command[1])
        artist = ""
        for word in words:
            if(word == "_"):
                artist += " "
            else:
                artist += word
        try:
            res = preview_music(artist)
        except requests.exceptions.HTTPError:
            bot.reply_to(message, 'HTTP error occurs, please try again in a minute')
        except ConnectionError:
            bot.reply_to(message, 'Connection error occurs, please try again in a minute')
        except PermissionError:
            bot.reply_to(message, 'Please stop the audio file before requesting new file')
        else:
            if res == "success":
                photo = open(get_path('utils/itunes-logo.png'), 'rb')
                audio = open(get_path('utils/preview.mp3'), 'rb')
                bot.send_photo(message.chat.id, photo)
                bot.send_audio(message.chat.id, audio)
            else:
                bot.reply_to(message, res)


def get_path(file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file))


@bot.message_handler(commands=['apod'])
def apod(message):
    app.logger.debug("'apod' command detected")

    try:
        apod = fetch_apod()
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, 'A connection error occured. Please try again in a moment.')
    except requests.exceptions.HTTPError:
        bot.reply_to(message, 'An HTTP error occured. Please try again in a moment.')
    except requests.exceptions.RequestException:
        bot.reply_to(message, 'An error occured. Please try again in a moment.')
    except ValueError as e:
        bot.reply_to(message, '/apod doesn\'t need any arguments')
    else:
        bot.reply_to(message, apod)


@bot.message_handler(regexp=r'^/hospital$')
def hospital(message):
    app.logger.debug("'hospital' command detected")
    chat_id = message.chat.id
    message_id = message.message_id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Share Location', request_location=True)
    markup.row(button)
    text = "Please share your location so we can get your nearest hospital!"
    msg = bot.send_message(chat_id, text, message_id, reply_markup=markup)
    bot.register_next_step_handler(msg, get_user_location_hospital)


@bot.message_handler(regexp=r'^/random_hospital$')
def random_hospital(message):
    app.logger.debug("'random_hospital' command detected")
    chat_id = message.chat.id
    message_id = message.message_id
    rs_list = lookup_random_hospital()
    markup = types.InlineKeyboardMarkup()
    for rs in rs_list:
        text = "Rumah Sakit " + rs['nama']
        callback = "RS_ID=" + str(rs['id'])
        butt = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(butt)
    text = "Please select one hospital below!"
    bot.send_message(chat_id, text, message_id, reply_markup=markup)


def get_user_location_hospital(message):
    app.logger.debug("'get user location for hospital' handler executed")
    chat_id = message.chat.id
    lat = message.location.latitude
    long = message.location.longitude
    rs = lookup_hospital(long, lat)
    reply_hospital(chat_id, rs)


@bot.callback_query_handler(func=lambda call: True)
def parse_callback(call):
    message = call.message
    data = call.data
    chat_id = message.chat.id
    if len(data.split("RS_ID=")) == 2:
        rs_id = data.split("RS_ID=")[1]
        rs = reply_random_hospital(rs_id)
        reply_hospital(chat_id, rs)


def reply_hospital(chat_id, rs):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, "Here is the result:", reply_markup=markup)
    bot.send_location(chat_id, rs['lat'], rs['long'])
    bot.send_photo(chat_id, urllib.request.urlopen(rs['image']).read())
    bot.send_message(chat_id, rs['message'])
    if 'distance' in rs:
        bot.send_message(chat_id, rs['distance'])


def check_from_group(message):
    return message.chat.type == "group"


@bot.message_handler(regexp=r'darurat', func=check_from_group)
def ask_darurat_location(message):
    app.logger.debug("'darurat' handler executed")
    chat_id = message.chat.id
    text = "Please share your location so we can get your nearest hospital!"
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, get_user_location_hospital)
