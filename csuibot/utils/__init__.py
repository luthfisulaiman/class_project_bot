from csuibot.utils import message_dist as md
import json
import urllib.request
import re
import time
import urllib.error
import requests
from bs4 import BeautifulSoup
from csuibot.utils import (zodiac as z, ip, palindrome as p, hipster as hp,
                           loremipsum as li, hex2rgb as h, xkcd as x, meme,
                           password as pw, custom_chuck as cc, kelaskata as k,
                           define as d, yelkomputer, soundcomposer as sc,
                           calculate_binary as cb, isUpWeb as iuw, notifTaker as n,
                           compute as co, definisi, note, dayofdate as dod, news,
                           chuck, discretemath as dm, marsfasilkom, yelfasilkom,
                           wiki, xkcd2 as x2, similar,
                           billboard_hot100_artist as felh,
                           billboard_newage_artist as feln,
                           billboard_hotcountry_artist as felhc,
                           oricon_cd as ocd, billboard as b, hotcountry as hot,
                           newage as na, fakejson, detectlang, billArtist as ba, weton,
                           books, youtube, japanartist as ja, extractcolour,
                           topTropical as trop, mangaTopOricon as mto, tagging,
                           twitter_search as ts, aqi)


def lookup_zodiac(month, day):
    zodiacs = [
        z.Aries(),
        z.Taurus(),
        z.Gemini(),
        z.Cancer(),
        z.Leo(),
        z.Virgo(),
        z.Libra(),
        z.Scorpio(),
        z.Sagittarius(),
        z.Capricorn(),
        z.Aquarius(),
        z.Pisces()
    ]

    for zodiac in zodiacs:
        if zodiac.date_includes(month, day):
            return zodiac.name
    else:
        return 'Unknown zodiac'


def lookup_chinese_zodiac(year):
    num_zodiacs = 12
    zodiacs = {
        0: 'rat',
        1: 'buffalo',
        2: 'tiger',
        3: 'rabbit',
        4: 'dragon',
        5: 'snake',
        6: 'horse',
        7: 'goat',
        8: 'monkey'
    }
    ix = (year - 4) % num_zodiacs

    try:
        return zodiacs[ix]
    except KeyError:
        return 'Unknown zodiac'


def lookup_sentiment_new(text):
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    sentiment_api = 'text/analytics/v2.0/sentiment'
    sentimentUri = base_url + sentiment_api
    apiKey = '4c831ddf14ba43bd98d6f1aa527b3de6'
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = apiKey
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    postData1 = json.dumps({"documents": [{"id": "1", "language": "en", "text": text}]})
    postData2 = postData1.encode('utf-8')
    request2 = urllib.request.Request(sentimentUri, postData2, headers)
    response2 = urllib.request.urlopen(request2)
    response2json = json.loads(response2.read().decode('utf-8'))
    sentiment = response2json['documents'][0]['score']
    return ('Sentiment:  %f' % sentiment)


def get_aqi_coord(coord):
    return aqi.GetAQICoord(coord)


def get_aqi_city(city):
    return aqi.GetAQICity(city)


def get_tweets(user):
    return ts.Twitter_Search().get_tweets(user)


def define_sound(inputKey):

    title = inputKey.split(' ', 1)[1]
    soundtitle = title.replace(" ", "_") + ".mp3"

    return 'soundclip/' + soundtitle


def word_feats(words):
    return dict([(word, True) for word in words])


def get_oricon_books(date):
    return books.Books().get_top_10(date)


def lookup_wiki(term):
    if term == '':
        raise ValueError('Command /wiki need an argument')
    else:
        object_wiki = wiki.Wiki(term)
        try:
            return object_wiki.get_result()
        except Exception as e:
            raise IndexError(
                'Page id "' + term + '" does not match any pages.'
                                     ' Try another id!'
            )


def lookup_message_dist(chat_id):
    message_dist = md.get_message_dist()
    message_dist_text = ''
    total_message = 0

    for hour in range(0, 24):
        total_message += message_dist['dist'][str(chat_id)][str(hour)]

    for hour in range(0, 24):
        idx_hour = 0
        idx_percent = 0
        try:
            val = message_dist['dist'][str(chat_id)][str(hour)] * 100.0
            idx_percent = float(val) / total_message
        except ZeroDivisionError:
            percent_at_specified_hour = 0.0
            idx_hour = str(hour).zfill(2)
            idx_percent = str(round(percent_at_specified_hour, 2))
        message_dist_text += '{} -> {}%\n'.format(idx_hour, idx_percent)

    return message_dist_text


def add_message_dist(chat_id, hour):
    md.add_message_to_dist(chat_id, hour)


def lookup_marsfasilkom(message_text):
    if message_text == '/marsfasilkom':
        return marsfasilkom.MarsFasilkom.get_mars_fasilkom()
    else:
        raise ValueError('Command /marsfasilkom doesn\'t need any arguments')


def lookup_yelfasilkom(message_text):
    if message_text == '/yelfasilkom':
        return yelfasilkom.YelFasilkom.get_yel_fasilkom()
    else:
        raise ValueError('Command /yelfasilkom doesn\'t need any arguments')


def call_discrete_material(query):
    return dm.DiscreteMath().get_discrete_material(query)


def manage_notes(command, text=''):
    note_obj = note.Notes(text)

    if command == 'view':
        try:
            return note_obj.view()
        except (FileNotFoundError, json.JSONDecodeError):
            return 'No notes yet'
    elif command == 'add':
        return note_obj.write()


def lookup_definisi(word):
    kamus = definisi.Definisi()

    mean = kamus.define(word)

    return mean


def takeSceleNotif():
    notif = n.notifTaker()
    return notif.getPost()


def checkTopTropical(artist):
    topTropical = trop.topTropicalBb()
    return topTropical.checkTopTropical(artist)


def getTopManga(year, month, day):
    manga = mto.mangaTopOricon()
    try:
        hasil = manga.getTopManga(str(year), str(month), str(day))
    except urllib.error.URLError as err:
        if(err.code == 404):
            return "Page not found, you may gave incorrect date"
        else:
            return "unexpected Error Happened"
    return hasil


def getTopMangaMonthly(year, month):
    manga = mto.mangaTopOricon()
    try:
        hasil = manga.getTopMangaMonthly(str(year), str(month))
    except urllib.error.URLError as err:
        if(err.code == 404):
            return "Page not found, you may gave incorrect date"
        else:
            return "unexpected Error Happened"
    return hasil


def lookup_isUpWeb(url):
    pattern = re.compile("^(https?)://[^\s/$.?#].[^\s]*$")
    if (pattern.match(url)):
        return iuw.IsUpWeb(url).isUp()
    else:
        raise ValueError


def remind_me(second, text):
    s = int(second)
    if (s > 30):
        raise Exception
    while (s > 0):
        time.sleep(1)
        s -= 1
    return text


def calculate_binary(binA, operand, binB):
    if operand == '+':
        return str(cb.CalculateBinary(binA, binB).addition())
    elif operand == '-':
        return str(cb.CalculateBinary(binA, binB).subtraction())
    elif operand == '*':
        return str(cb.CalculateBinary(binA, binB).multiplication())
    else:
        return str(cb.CalculateBinary(binA, binB).division())


def lookup_define(word):
    if (not word):
        raise ValueError('Command /define need an argument')
    elif (containsDigit(word)):
        return word + ' contains number'
    else:
        define_object = d.define(word)
        return define_object.getDefine()


def containsDigit(string):
    return any(i.isdigit() for i in string)


def lookup_kelaskata(message):
    if message == '':
        raise ValueError('Try /kelaskata [word]')
    else:
        kelaskata_object = k.kelaskata(message)
        return kelaskata_object.getKelasKata()


def generate_custom_chuck_joke(first_name, last_name):
    return cc.CustomChuckJoke().generate_custom_chuck_joke(first_name, last_name)


def generate_password(len):
    return pw.Password().generate_password(len)


def get_public_ip():
    return ip.IP().ip()


def make_hipster(paras):
    generator = hp.HipsterGenerator()

    try:
        return generator.generate(paras)
    except ValueError:
        return 'Number of paragraph exceed the limit'


def get_meme(top, bottom):
    generator = meme.MemeGenerator()
    generator.createid()
    try:
        generator.createtop(top)
        generator.createbottom(bottom)
    except ValueError:
        return 'Caption is too long, min < 100 words'
    else:
        dank = generator.generatememe()
        return dank.getimage()


def check_palindrome(message):
    _, text = message.text.split(' ')
    return p.Palindrome(text).is_palindrome()


def call_lorem_ipsum():
    return li.LoremIpsum().get_loripsum()


def fetch_latest_xkcd():
    return x.Comic.get_latest_comic()


def convert_hex2rgb(hex_str):
    return h.Hex2RGB(hex_str).convert()


def lookup_yelkomputer(message_text):
    if message_text == '/yelkomputer':
        return yelkomputer.YelKomputer.get_yel_komputer()
    else:
        raise ValueError('Command /yelkomputer doesn\'t need any arguments')


def compute(message):
    _, text = message.text.split(' ')
    return co.Compute(text).calculate()


def call_composer(username):
    return sc.SoundComposer(username).get_composer()


def lookup_dayofdate(year, month, day):
    try:
        return dod.dayofdate.dayoutput(year, month, day)
    except ValueError:
        return ('Incorrect use of dayofdate command. '
                'Please write a valid date in the form of yyyy-mm-dd, '
                'such as 2016-05-13')


def similar_text(input1, input2):
    checker = similar.SimilarText()
    try:
        if (input1[0:7] == "http://" or input1[0:8] == "https://"):
            if (input2[0:7] == "http://" or input2[0:8] == "https://"):
                return checker.checkweb(input1, input2)

        return checker.checktext(input1, input2)

    except requests.exceptions.ConnectionError:
        return "Connection Error occurs, please check your url or try again later"
    except ValueError:
        return "Your input is too long, please keep below 500 words"


def lookup_top10_billboard_chart(chart_category):
    result = b.get_top10(chart_category)
    if result != 'Invalid chart category':
        result_rank = ''
        for i in range(0, 10):
            rank_i = result['items'][i]
            title = rank_i.find('title').text
            artist = rank_i.find('artist').text
            current_rank = rank_i.find('rank_this_week').text
            result_rank += '({}) - {} - {} \n'.format(current_rank, artist, title)
        return result_rank
    return result


def top_ten_cd_oricon(chart_type, date):
    chart = ocd.Oricon_cd.get_top_ten(chart_type, date)
    return chart


def find_hot100_artist(name):
    try:
        return felh.Hot100_artist().find_hot100_artist(name)
    except ValueError:
        return ("Artist is not present on chart or no such artist exists\n"
                "Artist's name is case sensitive")


def find_newage_artist(name):
    try:
        return feln.NewAge_artist().find_newage_artist(name)
    except ValueError:
        return ("Artist is not present on chart or no such artist exists\n"
                "Artist's name is case sensitive")


def find_hotcountry_artist(name):
    try:
        return felhc.HotCountry_artist().find_hotcountry_artist(name)
    except ValueError:
        return ("Artist is not present on chart or no such artist exists\n"
                "Artist's name is case sensitive")


def lookup_hotcountry():
    hotcountry_object = hot.hotcountry()
    return hotcountry_object.getHotcountry()


def get_comic(id):
    comic_gen = x2.Xkcd2Generator()
    try:
        img = comic_gen.get_img(id)
    except ValueError:
        return 'Cant\'t found requested comic. Please ensure that your input is correct'
    except requests.exceptions.HTTPError:
        return 'Cant\'t found requested comic. Please ensure that your input is correct'
    else:
        return img


def get_chuck(message_text):
    if message_text == "/chuck":
        return chuck.Chuck().get_chuck()
    else:
        raise ValueError('Command /chuck doesn\'t need any arguments')


def get_articles(message_text):

    articles = news.News().get_news(message_text)

    brackets = '========================='
    out = brackets + '\n\n'
    for values in articles['value'][0:5]:
        out += ("[" + values['name'] + "]\n\n")
        out += (values['description'] + "\n")
        out += ("LINK: " + values['url'] + "\n\n")
        out += brackets + '\n\n'
    res = {'type': articles['_type'], 'value': out}
    return res


def lookup_HotJapan100(html):
    string = ''
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('title')[1:11]
    artist = soup.find_all('artist')[1:11]
    for i in range(10):
        if i < 9:
            string += '(' + str(i+1) + ') ' + title[i].string[3:] + "-" + artist[i].string
            string += '\n'
        elif i == 9:
            string += '(' + str(i+1) + ') ' + title[i].string[4:] + "-" + artist[i].string
            string += '\n'
    return (string)


def lookup_url(url):
    return youtube.Youtube().getURL(url)


def lookup_artist(artist):
    return ja.JapanArtist().getArtist(artist)


def get_fake_json(arg):
    if arg is '':
        return fakejson.FakeJson().get_response()
    raise ValueError('Command /fake_json doesn\'t need any arguments')


def lookup_newage():
    newage_object = na.newage()
    return newage_object.getNewage()


def extract_colour(message):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    ec = extractcolour.ExtractColour(photo_id)
    if caption == "/fgcolour":
        ec.state = extractcolour.ExtractColour.FGCOLOUR
    ret = ec.extract()
    return ret


def lookup_billArtist(message):
    try:
        billArtist_object = ba.billArtist(message)
        return billArtist_object.getBillArtist()
    except ValueError:
        return message + " doesn't exist in bill200"


def lookup_lang(arg):
    if arg is '':
        raise ValueError('Command /detect_lang need an argument')

    request = detectlang.DetectLang(arg)
    return request.get_result()


def lookup_weton(year, month, day):
    try:
        return weton.Weton(year, month, day).get_weton()
    except TypeError:
        return 'Year/Month/Day is invalid'
    except ValueError:
        return 'Year/Month/Day is invalid'


def auto_tag(message):
    photoid = message.photo[-1].file_id
    return tagging.Tagging(photoid).getTag()


def save_mediawiki_url(url):
    pass


def get_mediawiki(args):
    pass
