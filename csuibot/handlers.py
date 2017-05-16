from . import app, bot
import requests
import re
import urllib
from .utils import (lookup_zodiac, lookup_chinese_zodiac, check_palindrome,
                    call_lorem_ipsum, lookup_yelkomputer, get_public_ip,
                    convert_hex2rgb, fetch_latest_xkcd, make_hipster,
                    get_meme, generate_password, get_chuck, generate_custom_chuck_joke,
                    lookup_define, lookup_kelaskata, call_composer, calculate_binary,
                    remind_me, lookup_isUpWeb, takeSceleNotif, lookup_definisi,
                    manage_notes, lookup_dayofdate, compute, call_discrete_material,
                    lookup_message_dist, add_message_dist, lookup_wiki, get_comic,
                    lookup_marsfasilkom, lookup_yelfasilkom, data_processor, similar_text,
                    find_hot100_artist, find_newage_artist, find_hotcountry_artist,
                    top_ten_cd_oricon, lookup_top10_billboard_chart,
                    lookup_hotcountry, lookup_newage, get_fake_json, lookup_lang,
                    lookup_billArtist, lookup_weton, get_oricon_books,
                    lookup_url, lookup_artist, extract_colour, checkTopTropical,
                    getTopManga, getTopMangaMonthly, auto_tag, lookup_sentiment,
                    lookup_HotJapan100)
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


@bot.message_handler(regexp=r'^/sentiment \w+')
def sentiment(message):
    app.logger.debug("'sentiment' command detected")
    _, word_str = message.text.split(' ', 1)
    word_str = word_str.lower()
    word = lookup_sentiment(word_str)
    bot.reply_to(message, word)


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


@bot.message_handler(regexp=r'/billboard (tropicial|hot100|200)$')
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
