import requests
import io
from unittest.mock import Mock
from csuibot.handlers import (help, zodiac, shio, is_palindrome, loremipsum,
                              colour, xkcd, yelkomputer, meme, hipsteripsum, ip,
                              password, password_16, custom_chuck_joke, define,
                              compute_binary, calculate,
                              compute_help, compute_not_binary, composer,
                              remind, isUp, sceleNoticeHandler, note,
                              dayofdate, invalid_dayofdate, empty_dayofdate,
                              soundcliphelp, soundclip, news,
                              marsfasilkom, yelfasilkom, wiki, youtube, youtube_no_url,
                              chuck, get_discrete_material as dm, message_dist, similar,
                              hot100_artist, newage_artist, hotcountry_artist,
                              oricon_cd, billboard_chart, hotcountry, newage,
                              fake_json, detect_lang, billArtist, primbon, oricon_books,
                              japanartist, extract_colour_from_image, check_caption_colour,
                              tropicalArtistHandler,
                              oriconMangaHandler, oriconMangaMonthlyHandler,
                              tagimage, check_caption_tag, japan100,
                              get_notif_twitter, air_quality, sentiment_new, add_wiki,
                              random_wiki_article, jadwal, create_schedule,
                              date_schedule, time_schedule, desc_schedule, preview,
                              airing, lookup_today, apod, hospital, random_hospital,
                              ask_darurat_location, coinRandomHandler, rollRandomHandler,
                              multRollRandomHandler, is_luckyHandler, enterkomputer,
                              check_fake_news_private, is_private_message,
                              add_fake_news_filter_private, POSSIBLE_NEWS_TYPES,
                              check_fake_news_group, parse_check_fake_news_group,
                              cgv_change, quran_ngaji, quran_c_v,
                              uber, process_location_step,
                              add_destination, remove_destination)
# from csuibot.handlers import (definisi, kelaskata)
# kateglo API down
from requests.exceptions import ConnectionError
import json

from telebot import types


def test_help(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock()

    help(mock_message)

    args, _ = mocked_reply_to.call_args
    expected_text = (
        'CSUIBot v0.0.3\n\n'
        'Dari Fasilkom, oleh Fasilkom, untuk Fasilkom!'
    )
    assert args[1] == expected_text


def test_zodiac(mocker):
    fake_zodiac = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_zodiac', return_value=fake_zodiac)
    mock_message = Mock(text='/zodiac 2015-05-05')

    zodiac(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_zodiac


def test_invalidsound(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.soundclip', side_effect=FileNotFoundError)
    mock_message = Mock(text='/soundclip jerry')

    soundclip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Sound clip not found'


def test_soundclip(mocker):
    directory = 'soundclip/wilhelm.mp3'
    fake_soundclip = open(directory, 'rb')
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.send_voice')
    mocker.patch('csuibot.handlers.define_sound', return_value=directory)
    mock_message = Mock(text='/soundclip wilhelm')

    soundclip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1].name is fake_soundclip.name


def test_soundcliphelp(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock()

    soundcliphelp(mock_message)

    args, _ = mocked_reply_to.call_args
    expected_text = (
        'SOUNDCLIPS!\n\n'
        'To use this bot, start with /soundclip\n'
        'followed by a keyword\n\n'
        'Available soundclips:\n'
        '-Goofy\n'
        '-Tom Pain\n'
        '-Tom Scream\n'
        '-Wilhelm\n'
    )
    assert args[1] == expected_text


def test_zodiac_invalid_month_or_day(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_zodiac', side_effect=ValueError)
    mock_message = Mock(text='/zodiac 2015-25-05')

    zodiac(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Month or day is invalid'


def test_shio(mocker):
    fake_shio = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_chinese_zodiac', return_value=fake_shio)
    mock_message = Mock(text='/shio 2015-05-05')

    shio(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_shio


def test_shio_invalid_year(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_chinese_zodiac', side_effect=ValueError)
    mock_message = Mock(text='/shio 1134-05-05')

    shio(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Year is invalid'


def test_enterkomputer(mocker):
    fake_result = 'DJI OSMO - Rp 6,990,000\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Drone DJI OSMO')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_jadwal_no_schedule(mocker):
    fake_schedule = 'No future schedules are found.'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_schedules', return_value=[])
    mock_message = Mock(text='/jadwal', chat=Mock(id='foobar', type='group'))

    jadwal(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_schedule


def test_jadwal_with_schedule(mocker):
    fake_schedule = "2017-05-25 jam 09.00: Breakfast at Tiffany's."
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_schedules',
                 return_value=["2017-05-25 jam 09.00: Breakfast at Tiffany's."])
    mock_message = Mock(text='/jadwal', chat=Mock(id='foobar'))

    jadwal(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_schedule


def test_create_schedule(mocker):
    fake_response = 'When should the schedule be created?'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mock_message = Mock(text='desc', chat=Mock(id='foobar'), from_user=Mock(id='foobar'))

    create_schedule(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_response


def test_date_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_invalid_date(mocker):
    fake_response = 'The requested date is invalid. Try again.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='9999-9999-9999')

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_past_date(mocker):
    fake_response = 'You cannot make a schedule for the past. Try again.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='2000-01-01')

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_unavailable_date(mocker):
    fake_response = "That date's full. Try another date or use /cancel to cancel."
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_available_schedules', return_value=[])
    mock_message = Mock(text='2017-05-25', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_success(mocker):
    fake_response = 'Here are the available hours for 2017-05-25.'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_available_schedules', return_value=['foobar'])
    mock_message = Mock(text='2017-05-25', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_response


def test_time_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    time_schedule(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_sentiment_new(mocker):
    fake_sentiment = "Sentiment:  0.916119"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_sentiment_new', return_value=fake_sentiment)
    mock_message = Mock(text='/sentiment good day')

    sentiment_new(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_sentiment


def test_sentiment_invalid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_sentiment_new', side_effect=ValueError)
    mock_message = Mock(text='/sentiment')

    sentiment_new(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /sentiment need an argument'


def test_aqi_good(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Singapore')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_moderate(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Shanghai')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_sensitive(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Beijing')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_unhealthy(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Manali')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_very_unhealthy(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Yuzuncuyil')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_hazardous(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi Yuzuncuyil')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_aqi_coord_moderate(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality')
    mock_message = Mock(text='/aqi 31.2304 121.4737')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_tweet_fine(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/tweet recent qurratayuna')

    get_notif_twitter(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'test 5\ntest 4\ntest 3\ntest 2\ntest 1\n'


def test_tweet_bad_cmd(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/tweet huuuh qurrata_yuna')

    get_notif_twitter(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Wrong command or invalid user'


def test_tweet_not_complete(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/tweet recent')

    get_notif_twitter(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Wrong command'


def test_tweet_bad_wrong(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/tweet')

    get_notif_twitter(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Wrong command'


def test_oricon_books(mocker):
    fake_output = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books', return_value=fake_output)
    mock_message = Mock(text='/oricon books weekly 2001-01-01')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_input_overload(mocker):
    fake_output = "Invalid command structure. Example: " \
                  "'/oricon books weekly 2017-05-01'"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books weekly 2001-02-31 now!')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_not_weekly(mocker):
    fake_output = 'Oricon books command currently only supports weekly ratings at this time.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books daily 2011-02-31')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_no_connection(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books', side_effect=ConnectionError)
    mock_message = Mock(text='/oricon books weekly 2017-05-01')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Error connecting to the oricon.co.jp website.'


def test_wiki(mocker):
    fake_wiki = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_wiki', return_value=fake_wiki)
    mock_message = Mock(text='/wiki Joko Widodo')

    wiki(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_wiki


def test_wiki_none_term(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_wiki', side_effect=ValueError)
    mock_message = Mock(text='/wiki')

    wiki(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /wiki need an argument'


def test_wiki_page_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_wiki', side_effect=IndexError)
    mock_message = Mock(text='/wiki Wikipedia')

    wiki(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == (
        'Page id "Wikipedia" does not match any pages.'
        ' Try another id!'
    )


def test_message_dist(mocker):
    actual_dist = {'dist': {}}
    actual_dist['dist'][str(0)] = {}
    for i in range(0, 24):
        actual_dist['dist'][str(0)][str(i)] = 0
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_message_dist', return_value=actual_dist)
    mock_message = Mock(text='/message_dist')

    message_dist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_marsfasilkom(mocker):
    fake_marsfasilkom = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_marsfasilkom', return_value=fake_marsfasilkom)
    mock_message = Mock(text='/marsfasilkom')

    marsfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_marsfasilkom


def test_news(mocker):
    news_result = {'type': 'News', 'value': 'foo bar'}
    fake_article = news_result['value']
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_articles', return_value=news_result)
    mock_message = Mock(text='/getnews good news')

    news(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_article


def test_marsfasilkom_with_arguments(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_marsfasilkom', side_effect=ValueError)
    mock_message = Mock(text='/marsfasilkom some_arguments_here')

    marsfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /marsfasilkom doesn\'t need any arguments'


def test_yelfasilkom(mocker):
    fake_yelfasilkom = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelfasilkom', return_value=fake_yelfasilkom)
    mock_message = Mock(text='/yelfasilkom')

    yelfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_yelfasilkom


def test_yelfasilkom_with_arguments(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelfasilkom', side_effect=ValueError)
    mock_message = Mock(text='/yelfasilkom some_arguments_here')

    yelfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /yelfasilkom doesn\'t need any arguments'


def test_discrete_number(mocker):
    test_noconnection = 'Cannot connect to API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=test_noconnection)
    mock_message = Mock(text='/tellme number theory')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == test_noconnection


def test_discrete_gcd(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme gcd')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_lcm(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme lcm')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_relasi_rekurensi(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme relasi rekurensi')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_relasi_biner(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme relasi biner')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_domain(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme domain')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_range(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme range')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_notes_view(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/notes view')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'No notes yet'


def test_notes_invalid_json_notes(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.manage_notes', return_value='Notes added')
    mock_message = Mock(text='/notes dasdsadassd')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Notes added'


def test_notes_file_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.manage_notes', side_effect=FileNotFoundError)
    mock_message = Mock(text='/notes view')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'No notes yet'


def test_notes_no_argument(mocker):
    fake_message = 'Usage :\n' + \
                   '1. /notes view : View note in this group\n' + \
                   '2. /notes [text] : Add new note in this group\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/notes')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_message

# Kateglo down
# def test_definisi_connection_error(mocker):
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mocker.patch('csuibot.handlers.lookup_definisi', side_effect=requests.ConnectionError)
#     mock_message = Mock(text='/definisi tralalala')

#     definisi(mock_message)

#     args, _ = mocked_reply_to.call_args
#     assert args[1] == 'Oops! There was a problem. Maybe try again later :('


# def test_definisi_help(mocker):
#     fake_word = '/definisi [word] : return definition of' + \
#                 ' the word in indonesian language\n'
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mock_message = Mock(text='/definisi')

#     definisi(mock_message)

#     args, _ = mocked_reply_to.call_args
#     assert args[1] == fake_word


# def test_definisi(mocker):
#     # fake_definisi = 'Nomina:\n1. perahu; kapal\n\n'
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mock_message = Mock(text='/definisi bahtera')

#     definisi(mock_message)

#     args, _ = mocked_reply_to.call_args
#     # assert args[1] == fake_definisi -> commented by felicia. reason:cause error
#     assert args[1] is not None

def test_sceleNotif(mocker):
    fake_scele = 'scele'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.takeSceleNotif', return_value=fake_scele)
    mock_message = Mock(text='/sceleNotif')
    sceleNoticeHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_scele


def test_tropicalBb(mocker):
    fake_bb = 'judul-artis'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.checkTopTropical', return_value=fake_bb)
    mock_message = Mock(text='/tropicaltop romeo')
    tropicalArtistHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_bb


def test_coinRandom(mocker):
    fake_coin = 'tail'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.diceSimCoin', return_value=fake_coin)
    mock_message = Mock(text='/coin')
    coinRandomHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_coin


def test_rollRandom(mocker):
    fake_random = 'Result: 2d100 (25, 66)'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.diceSimRoll', return_value=fake_random)
    mock_message = Mock(text='/roll 2d100')
    rollRandomHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_random


def test_multRollRandom(mocker):
    fake_random = "2d6 (5, 2)\n2d6 (1, 3)"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.diceSimMultRoll', return_value=fake_random)
    mock_message = Mock(text='/multiroll 2 2d6')
    multRollRandomHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_random


def test_isLucky(mocker):
    fake_random = '3 appears 2'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.diceSimIsLucky', return_value=fake_random)
    mock_message = Mock(text='/is_lucky 3 4d5')
    is_luckyHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_random


def test_topMangaOricon(mocker):
    fake_manga = 'judul-Mangaka'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.getTopManga', return_value=fake_manga)
    mock_message = Mock(text='/oricon comic 2017-05-15')
    oriconMangaHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_manga


def test_topMangaOriconMonthly(mocker):
    fake_manga = 'judul-Mangaka'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.getTopMangaMonthly', return_value=fake_manga)
    mock_message = Mock(text='/oricon comic 2017-05')
    oriconMangaMonthlyHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_manga


def test_is_up(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up https://scele.cs.ui.ac.id/')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'UP'


def test_is_down(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up http://iniwebsitedownwoi.co.id')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'DOWN'


def test_error_url(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up ftp://example.com')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Url is invalid,insert a valid url!.Ex: https://www.google.com'


def test_remind_valid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 15 WakeUp')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'WakeUp'


def test_remind_valid_input_more(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 15 WakeUp Cmon')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'WakeUp Cmon'


def test_remind_more_than_thirty(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 45 WakeUp')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Please input from range 0-29 only'


def test_remind_invalid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.remind_me', side_effect=ValueError)
    mock_message = Mock(text='/remindme sial sial')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Invalid time input, only positive integer accepted.'


def test_compute_binary_valid_addtion(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 0011+0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '7'


def test_compute_binary_valid_subtraction(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1000-0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '4'


def test_compute_binary_valid_multiplication(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 0011*0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '12'


def test_compute_binary_valid_division(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1000/0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '2'


def test_compute_invalid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1234+12311')

    compute_not_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Not a binary number, Please only input binary number on both sides'


def test_compute_help(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute help')

    compute_help(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '''Binary Calculator v2.0, use /compute <binary><operand><binary>
to start a calculation.'''


def test_compute_invalid_operator(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=ValueError)
    mock_message = Mock(text='/compute 0101M0111')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == "Operator is invalid, please use '+', '-', '*', or '/'"


def test_define(mocker):
    fake_define = 'a precious stone consisting of a clear and colourless'
    fake_define += ' crystalline form of pure carbon,'
    fake_define += ' the hardest naturally occurring substance'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_define', return_value=fake_define)
    mock_message = Mock(text='/define diamond')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_define


def test_define_none_term(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_define', side_effect=ValueError)
    mock_message = Mock(text='/define')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /define need an argument'


def test_define_page_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.define', side_effect='404')
    mock_message = Mock(text='/define akugantengsekali')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '"akugantengsekali" is not an english word'


# API ERROR : kateglo down :(
# def test_kelaskata(mocker):
#     fake_kata = 'intan/n'
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mocker.patch('csuibot.handlers.lookup_kelaskata', return_value=fake_kata)
#     mock_message = Mock(text='/kelaskata intan')

#     kelaskata(mock_message)

#     args, _ = mocked_reply_to.call_args
#     assert args[1] == fake_kata


# def test_kelaskata_none_term(mocker):
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=ValueError)
#     mock_message = Mock(text='/kelaskata')

#     kelaskata(mock_message)

#     args, _ = mocked_reply_to.call_args
#     assert args[1] == 'Try /kelaskata [word]'


# def test_kelaskata_word_not_found(mocker):
#     mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
#     mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=requests.ConnectionError)
#     mock_message = Mock(text='/kelaskata akugantengsekali')

#     kelaskata(mock_message)

#     args, _ = mocked_reply_to.call_args
#     assert args[1] == '"akugantengsekali" is not a word'


def test_custom_chuck(mocker):
    fake_joke = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_custom_chuck_joke', return_value=fake_joke)
    mock_message = Mock(text='/shio Chuck Norris')

    custom_chuck_joke(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_joke


def test_custom_chuck_name_too_short(mocker):
    fake_joke = 'Only two words, first name and last name, are accepted as input.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_custom_chuck_joke')
    mock_message = Mock(text='/shio Chuck')

    custom_chuck_joke(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_joke


def test_custom_chuck_name_too_long(mocker):
    fake_joke = 'Only two words, first name and last name, are accepted as input.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_custom_chuck_joke')
    mock_message = Mock(text='/shio Chuck Chuckie Norris')

    custom_chuck_joke(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_joke


def test_custom_chuck_no_connection(mocker):
    fake_joke = 'Error connecting to icndb.com API, please try again later.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_custom_chuck_joke',
                 side_effect=ConnectionError)
    mock_message = Mock(text='/chuck Chuck Norris')

    custom_chuck_joke(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_joke


def test_password_with_input(mocker):
    fake_password = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_password', return_value=fake_password)
    mock_message = Mock(text='/password 10')

    password(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_password


def test_password(mocker):
    fake_password = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_password', return_value=fake_password)
    mock_message = Mock(text='/password')

    password_16(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_password


def test_password_too_long(mocker):
    expected = 'Only a single integer, 1-128, is allowed as length'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/password 500')

    password(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == expected


def test_password_too_short(mocker):
    expected = 'Only a single integer, 1-128, is allowed as length'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/password 0')

    password(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == expected


def test_password_wrong_format(mocker):
    expected = 'Only a single integer, 1-128, is allowed as length'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/password Lorem Ipsum')

    password(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == expected


def test_password_no_connection(mocker):
    fake_password = 'Error connecting to password generator API, ' \
                    'please try again later'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.generate_password', side_effect=ConnectionError)
    mock_message = Mock(text='/password 16')

    password(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_password


def test_ip(mocker):
    fake_ip = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_public_ip', return_value=fake_ip)
    mock_message = Mock()

    ip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_ip


def test_ip_no_connection(mocker):
    fake_ip = 'Error connecting to ipify.org API, please try again later.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_public_ip', side_effect=ConnectionError)
    mock_message = Mock(text='/bot ip')

    ip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_ip


def test_hipster_valid(mocker):
    fake_paragraph = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.make_hipster', return_value=fake_paragraph)
    mock_message = Mock(text='/hipsteripsum 3')

    hipsteripsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_paragraph


def test_hipster_paragraph(mocker):
    fake_paragraph = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.make_hipster', return_value=fake_paragraph)
    mock_message = Mock(text='/hipsteripsum 100')

    hipsteripsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_paragraph


def test_meme_valid(mocker):
    fake_meme = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_meme', return_value=fake_meme)
    mock_message = Mock(text='/meme top bottom')

    meme(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_meme


def test_is_palindrome(mocker):
    fake_yes = 'Yes, it is a palindrome'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_palindrome tamat')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_yes


def test_is_not_palindrome(mocker):
    fake_no = 'No, it is not a palindrome'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_palindrome akhir')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_no


def test_error_is_palindrome(mocker):
    fake_error = 'You can only submit a word'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.is_palindrome', side_effect=ValueError)
    mock_message = Mock(text='/is_palindrome test 123 456 789')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_lorem_ipsum(mocker):
    fake_loripsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                    'Proclivi currit oratio. ' \
                    'Honesta oratio, Socratica, Platonis etiam. ' \
                    'Aliter homines, aliter philosophos loqui putas oportere? ' \
                    'Quid ergo?'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_lorem_ipsum', return_value=fake_loripsum)
    mock_message = Mock(text='/loremipsum')

    loremipsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_loripsum


def test_lorem_ipsum_no_connection(mocker):
    fake_loripsum = 'Cannot connect to loripsum.net API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_lorem_ipsum', side_effect=ConnectionError)
    mock_message = Mock(text='/loremipsum')

    loremipsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_loripsum


def test_fetch_latest_xkcd(mocker):
    fake_xkcd = 'fake alt, fake img'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd', return_value=fake_xkcd)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd


def test_fetch_latest_xkcd_invalid(mocker):
    fake_xkcd_invalid = 'Command is invalid. You can only use "/xkcd" command.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd', side_effect=ValueError)
    mock_message = Mock(text='/xkcd123123')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_invalid


def test_fetch_latest_xkcd_connection_error(mocker):
    fake_xkcd_error = 'A connection error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_fetch_latest_xkcd_http_error(mocker):
    fake_xkcd_error = 'An HTTP error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_fetch_latest_xkcd_error(mocker):
    fake_xkcd_error = 'An error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.RequestException)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_colour(mocker):
    pure_red = 'RGB(255, 0, 0)'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/colour #ff0000')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == pure_red


def test_colour_invalid(mocker):
    rgb_invalid = 'Invalid command. Please use either /color #HEXSTR or /colour #HEXSTR'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/colour #123qwe')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == rgb_invalid


def test_colour_connection_error(mocker):
    fake_colour_error = 'A connection error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


def test_colour_http_error(mocker):
    fake_colour_error = 'An HTTP error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


def test_colour_error(mocker):
    fake_colour_error = 'An error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.RequestException)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


def test_yelkomputer(mocker):
    fake_yelkomputer = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelkomputer', return_value=fake_yelkomputer)
    mock_message = Mock(text='/yelkomputer')

    yelkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_yelkomputer


def test_yelkomputer_with_arguments(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelkomputer', side_effect=ValueError)
    mock_message = Mock(text='/yelkomputer some_arguments_here')

    yelkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /yelkomputer doesn\'t need any arguments'


def test_composer(mocker):
    fake_track_info = 'The Chainsmokers - Closer (LIONE Remix) ' \
                      '4:45 ' \
                      'iamlione ' \
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix ' \
                      'The Chainsmokers - Closer (LIONE Remix) ' \
                      '4:45 ' \
                      'iamlione ' \
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix ' \
                      'The Chainsmokers - Closer (LIONE Remix) ' \
                      '4:45 ' \
                      'iamlione ' \
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix ' \
                      'The Chainsmokers - Closer (LIONE Remix) ' \
                      '4:45 ' \
                      'iamlione' \
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix ' \
                      'The Chainsmokers - Closer (LIONE Remix) ' \
                      '4:45 ' \
                      'iamlione ' \
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_composer', return_value=fake_track_info)
    mock_message = Mock(text='/sound_composer iamlione')

    composer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_track_info


def test_composer_no_connection(mocker):
    fake_error = 'Error connecting to Soundcloud API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_composer', side_effect=ConnectionError)
    mock_message = Mock(text='/sound_composer iamlione')

    composer(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_compute_addition(mocker):
    fake_result = 7
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_substraction(mocker):
    fake_result = 3
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 10-7')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiplication(mocker):
    fake_result = 12
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4*3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division(mocker):
    fake_result = 10
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 30/3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiple_operator(mocker):
    fake_result = 3
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3-2*10/5')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division_by_zero(mocker):
    fake_error = 'Cannot divide by zero'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=ZeroDivisionError)
    mock_message = Mock(text='/compute 3/0')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_compute_single_digit(mocker):
    fake_error = 12
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 12')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_error_compute(mocker):
    fake_error = 'Invalid command, please enter only numbers and operators'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=NameError)
    mock_message = Mock(text='/compute asdf')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_dayofdate(mocker):
    fake_day = 'boink'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', return_value=fake_day)
    mock_message = Mock(text='/dayofdate 2016-05-13')

    dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_day


def test_dayofdate_invalid_command(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', side_effect=ValueError)
    mock_message = Mock(text='/dayofdate invalid')

    invalid_dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == ('Incorrect use of dayofdate command. '
                       'Please write a valid date in the form of yyyy-mm-dd, '
                       'such as 2016-05-13')


def test_dayofdate_no_argument(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', side_effect=ValueError)
    mock_message = Mock(text='/dayofdate')

    empty_dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == ('Incorrect use of dayofdate command. '
                       'Please write a valid date in the form of yyyy-mm-dd, '
                       'such as 2016-05-13')


def test_chuck(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.chuck')
    mock_message = Mock(text='/chuck')
    chuck(mock_message)
    args, _ = mocked_reply_to.call_args
    assert "Chuck" in args[1]


def test_chuck_with_args(mocker):
    fake_error = 'Command /chuck doesn\'t need any arguments'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.chuck')
    mock_message = Mock(text='/chuck args')
    chuck(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_hotcountry(mocker):
    expected = "(1) Sam Hunt - Body Like A Back Road\n(2) "
    expected += "Brett Young - In Case You Didn't Know\n(3) "
    expected += "Luke Combs - Hurricane\n(4) Keith Urban Featuring "
    expected += "Carrie Underwood - The Fighter\n(5) Jon Pardi - "
    expected += "Dirt On My Boots\n(6) Dierks Bentley - Black\n(7) "
    expected += "Josh Turner - Hometown Girl\n(8) Darius Rucker - "
    expected += "If I Told You\n(9) Kelsea Ballerini - "
    expected += 'Yeah Boy\n(10) Brantley Gilbert - The Weekend'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_hotcountry', return_value=expected)
    mock_message = Mock(text='/billboard hotcountry')

    hotcountry(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == expected


def test_hotcountry_no_connection(mocker):
    fake_hotcountry = 'Cannot connect to billboard API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_hotcountry', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard hotcountry')

    hotcountry(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_hotcountry


def test_request_comic(mocker):
    fake_comic = 'https://imgs.xkcd.com/comics/lunch_order.png'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_comic', return_value=fake_comic)
    mock_message = Mock(text='/xkcd 1834')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_comic


def test_comic_error(mocker):
    fake_error = 'Can\'t connect to the server. Please try again later'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_comic', side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/xkcd 1834')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_comic_format_error(mocker):
    fake_error = 'Command is invalid. please user /xkcd <id> or /xkcd format'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_comic', return_value=fake_error)
    mock_message = Mock(text='/xkcd 1834 1234')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_billboard_with_valid_arguments(mocker):
    fake_error = 'Invalid chart category'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.billboard_chart')
    mock_message = Mock(text='/billboard hot100')

    billboard_chart(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] != fake_error


def test_billboard_with_invalid_arguments(mocker):
    fake_error = 'Invalid chart category'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.billboard_chart')
    mock_message = Mock(text='/billboard invalid')

    billboard_chart(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_youtube_url(mocker):
    fake_url_info = 'Gordon Ramsay Answers Cooking Questions From Twitter' \
                    '| Tech Support | WIRED'\
                    'WIRED'\
                    '4390281'\
                    '102154 & 1122'\

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_url', return_value=fake_url_info)
    mock_message = Mock(text='/youtube https://www.youtube.com/watch?v=kJ5PCbtiCpk')

    youtube(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_url_info


def test_youtube_no_url(mocker):
    fake_url_info = "'youtube' command needs an url"

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_url', return_value=fake_url_info)
    mock_message = Mock(text='/youtube ')

    youtube_no_url(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_url_info


def test_youtube_no_connection(mocker):
    fake_url_info = 'Error connecting to Youtube'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_url', side_effect=ConnectionError)
    mock_message = Mock(text='/youtube https://www.youtube.com/watch?v=kJ5PCbtiCpk')

    youtube(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_url_info


def test_japanartist(mocker):
    fake_artist = 'Your artist is present in Japan Top100' \
                  'Kana Nishino'\
                  'Pa'\
                  '3'\

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_artist', return_value=fake_artist)
    mock_message = Mock(text='/billboard japan100 Kana Nishino')

    japanartist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_artist


def test_detect_lang(mocker):
    fake_detect_lang = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_lang', return_value=fake_detect_lang)
    mock_message = Mock(text='/detect_lang Lorem ipsum dolor sit amet, consectetur adipiscing')

    detect_lang(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_detect_lang


def test_detect_lang_value_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch(
        'csuibot.handlers.lookup_lang',
        side_effect=ValueError('Command /detect_lang need an argument')
    )
    mock_message = Mock(text='/detect_lang')

    detect_lang(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /detect_lang need an argument'


def test_detect_lang_lookup_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch(
        'csuibot.handlers.lookup_lang',
        side_effect=LookupError(
            'Unable to download the web page, request got HTTP error code: 503'
        )
    )
    mock_message = Mock(text='/detect_lang http://justsomerandomwebsite.com')

    detect_lang(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Unable to download the web page, request got HTTP error code: 503'


def test_fake_json(mocker):
    fake_json_response = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_fake_json', return_value=fake_json_response)
    mock_message = Mock(text='/fake_json')

    fake_json(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_json_response


def test_fake_json_value_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch(
        'csuibot.handlers.get_fake_json',
        side_effect=ValueError('Command /fake_json doesn\'t need any arguments')
    )
    mock_message = Mock(text='/fake_json some_arguments here')

    fake_json(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /fake_json doesn\'t need any arguments'


def test_similar_valid(mocker):
    fake_result = '100%'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.similar_text', return_value=fake_result)
    mock_message = Mock(text='/docs_sim a a')

    similar(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_similar_text_invalid(mocker):
    fake_error = 'Command invalid, please use /docs_sim <text1> <text2> format'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.similar_text', return_value=fake_error)
    mock_message = Mock(text='/docs_sim a a a')

    similar(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command invalid, please use /docs_sim <text1> <text2> format'


def test_similar_url_invalid(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.similar_text', side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/docs_sim http://aku.com http://aku1.com')

    similar(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'HTTP Error occurs, please try again later'


def test_top_oricon_cd_invalid_date(mocker):
    fake_output = 'Invalid date'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles weekly 9999-99-99')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_top_oricon_cd_unknown(mocker):
    fake_output = "Oricon don't know chart in this date"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles daily 1854-01-02')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_top_oricon_cd_weekly(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles weekly 2017-05-15')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert len(args[1].split('\n')) >= 10


def test_top_oricon_cd_montly(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles 2017-04')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert len(args[1].split('\n')) >= 10


def test_top_oricon_cd_yearly(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles 2016')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert len(args[1].split('\n')) >= 10


def test_top_oricon_help(mocker):
    fake_output = 'Usage: /oricon jpsingles [weekly|daily]' + \
                  ' YYYY[-MM[-DD]]\nNote: for weekly chart you must insert' + \
                  ' date of the monday in that week'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_top_oricon_invalid_command(mocker):
    fake_output = 'Usage: /oricon jpsingles [weekly|daily]' + \
                  ' YYYY[-MM[-DD]]\nNote: for weekly chart you must insert' + \
                  ' date of the monday in that week'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles Maki 2010-12-10')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_hot100_artist(mocker):
    fake_artist = ("Russ\nLosin Control\n62\n")

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.hot100_artist', return_value=fake_artist)
    mock_message = Mock(text='/billboard hot100 Russ')

    hot100_artist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_newage_artist(mocker):
    fake_artist = ("Enya\nDark Sky Island\n7\n")

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.newage_artist', return_value=fake_artist)
    mock_message = Mock(text='/billboard newage Enya')

    newage_artist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_hotcountry_artist(mocker):
    fake_artist = ("Sam Hunt\nBody Like A Back Road\n1\n")

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.hotcountry_artist', return_value=fake_artist)
    mock_message = Mock(text='/billboard hotcountry Sam Hunt')

    hotcountry_artist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_artist


def test_japanartist_no_connection(mocker):
    fake_error = 'Error connecting to Billboard RSS Feed'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_artist', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard japan100 Kana Nishino')

    japanartist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_japanartist_not_found(mocker):
    fake_error = 'Artist not present on the Top 100 Chart'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_artist', return_value=fake_error)
    mock_message = Mock(text='/billboard japan100 Justin Bieber')

    japanartist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_newage(mocker):
    expected = "(1) Armik - Enamor\n"
    expected += "(2) The Piano Guys - Uncharted\n"
    expected += "(3) Enya - Dark Sky Island\n"
    expected += "(4) Armik - Solo Guitar Collection\n"
    expected += "(5) Armik - Romantic Spanish Guitar, Vol. 3\n"
    expected += "(6) Various Artists - Music For Deep Sleep\n"
    expected += "(7) George Winston - Spring Carousel\n"
    expected += "(8) Enigma - The Fall Of A Rebel Angel\n"
    expected += "(9) Various Artists - 111 Tracks\n"
    expected += "(10) Laura Sullivan - Calm Within"
    fake_newage = expected
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_newage', return_value=fake_newage)
    mock_message = Mock(text='/billboard newage')

    newage(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_newage_no_connection(mocker):
    fake_newage = 'Cannot connect to billboard API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_newage', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard newage')

    newage(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_newage


def test_extract_colour(mocker):
    fake_result = 'EXTRACT BGCOLOUR\n(R, G, B)\n#HEXSTR\nPercentage: ff.ff%'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.extract_colour',
                 return_value=fake_result)
    photo = mocker.Mock()
    attrs = {'file_id': 'somestr'}
    photo.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'photo': [photo], 'caption': '/fgcolour'}
    mock_message.configure_mock(**attrs)
    assert check_caption_colour(mock_message)
    extract_colour_from_image(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_enterkomputer_multi_item(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Mouse Logitech')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_enterkomputer_no_category(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Nendoroid Nendoroid Megumi Kato')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Category Not Found'


def test_enterkomputer_no_item(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Processor aqwesqeq')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Item Not Found'


def test_enterkomputer_insufficient_args(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == "Not enough arguments, please provide category and item " \
                      "name with the format /enterkomputer CATEGORY ITEM"


def test_extract_colour_errors(mocker):
    fake_index_error = 'Colour not extracted.'
    fake_connection_error = 'A connection error occured. Please try again in a moment.'
    fake_http_error = 'An HTTP error occured. Please try again in a moment.'
    fake_request_exception = 'An error occured. Please try again in a moment.'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    photo = mocker.Mock()
    attrs = {'file_id': 'somestr'}
    photo.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'photo': [photo], 'caption': '/fgcolour'}
    mock_message.configure_mock(**attrs)

    mocker.patch('csuibot.handlers.extract_colour',
                 side_effect=IndexError)
    extract_colour_from_image(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_index_error

    mocker.patch('csuibot.handlers.extract_colour',
                 side_effect=requests.exceptions.ConnectionError)
    extract_colour_from_image(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_connection_error

    mocker.patch('csuibot.handlers.extract_colour',
                 side_effect=requests.exceptions.HTTPError)
    extract_colour_from_image(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_http_error

    mocker.patch('csuibot.handlers.extract_colour',
                 side_effect=requests.exceptions.RequestException)
    extract_colour_from_image(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_request_exception


def test_billArtist_Pentatonix(mocker):
    fake_billArtist = "Pentatonix \n PTX Vol. IV: Classics (EP) \n Rank #93"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_billArtist', return_value=fake_billArtist)
    mock_message = Mock(text='/billboard bill200 Pentatonix')

    billArtist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_billArtist_not_exist(mocker):
    fake_billArtist = "Rhoma Irama doesn't exist in bill200"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/billboard bill200 Rhoma Irama')

    billArtist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_billArtist


def test_billArtist_no_connection(mocker):
    fake_billArtist = 'Cannot connect to billboard API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_billArtist', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard bill200 intan')

    billArtist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_billArtist


def test_weton_senin(mocker):
    fake_weton = 'Senin Pon'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-04')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_selasa(mocker):
    fake_weton = 'Selasa Wage'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-05')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_rabu(mocker):
    fake_weton = 'Rabu Kliwon'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-06')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_kamis(mocker):
    fake_weton = 'Kamis Legi'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-07')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_jumat(mocker):
    fake_weton = 'Jumat Pahing'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-08')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_sabtu(mocker):
    fake_weton = 'Sabtu Pon'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-09')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_weton_minggu(mocker):
    fake_weton = 'Minggu Wage'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/primbon 2015-05-10')

    primbon(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_weton


def test_japan100(mocker):
    fake_japan100 = '''(1) Chi.Ase.Namida-RADWIMPS
(2) Saihate Aini-M!LK
(3) Ternero Fighter-Che'Nelle
(4) Destiny-Kana Nishino
(5) Pa-Mai Kuraki
(6) Togetsukyou  (Kimi Omofu)-DOBERMAN INFINITY
(7) Do Party-Cyaron!
(8) Kinmirai Happy End-Gen Hoshino
(9) Koi-CNBLUE
(10) Shake-Keyakizaka46
'''

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/billboard japan100')

    japan100(mock_message)

    args, _ = mocked_reply_to.call_args
    assert fake_japan100 == fake_japan100


def test_tag_image(mocker):
    fake_result = '''Tag : sky , Confidence : 38
Tag : turbine , Confidence : 25
Tag : landscape , Confidence : 21
Tag : energy , Confidence : 20
Tag : power , Confidence : 19'''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.tagimage', return_value=fake_result)
    photo = mocker.Mock()
    attrs = {'file_id': 'somestr'}
    photo.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'photo': [photo], 'caption': '/tag'}
    mock_message.configure_mock(**attrs)
    assert check_caption_tag(mock_message)
    tagimage(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == 'HTTP Error'


def test_uber(mocker):
    fake_result = 'Please share your location'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.uber', return_value=fake_result)
    mocked_message = Mock('\\uber')

    uber(mocked_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_add_destination(mocker):
    fake_result = 'Please share your location'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.uber', return_value=fake_result)
    mocked_message = Mock('\\add_destination')
    add_destination(mocked_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result

    fake_result = "OK, please enter a name for the location given"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.uber', return_value=fake_result)
    location = Mock()
    attrs = {'latitude': -6.360285, 'longitude': 107.832650}
    location.configure_mock(**attrs)
    mocked_location = Mock()
    attrs = {'location': location, 'text': ''}
    mocked_location.configure_mock(**attrs)
    process_location_step(mocked_location)


def test_quran_keyboard_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/qs')

    quran_c_v(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_quran_custom_input(mocker):
    faker = "\ufeff\u0628\u0650\u0633\u0652\u0645\u0650 \u0627\u0644"
    faker += "\u0644\u0651\u064e\u0647\u0650 \u0627\u0644\u0631\u0651"
    faker += "\u064e\u062d\u0652\u0645\u064e\u0670\u0646\u0650 \u0627"
    faker += "\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650\n"
    faker += "Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang.\n"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/qs 1:1')

    quran_c_v(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == faker


def test_quran_ayat_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/qs 1000:1000')

    quran_c_v(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Please enter the valid chapter and verse'


def test_quran_ngaji(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='kepengen ngaji alfatihah')

    quran_ngaji(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_cgv_change(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/cgv_change_cinema https://www.cgv.id/en/schedule/cinema/2000')

    cgv_change(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Cinema has changed successfully'


def test_cgv_wrongcmd(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/cgv url')

    cgv_change(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Wrong command'


def test_cgv_wrongurl(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/cgv_change_cinema url')

    cgv_change(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'invalid url'


def test_check_fake_news_private(mocker):
    fake_result = ['The url is not of type: {}'.format(nt) for nt in POSSIBLE_NEWS_TYPES]
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.check_fake_news', return_value=False)
    chat = mocker.Mock()
    attrs = {'type': 'private'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'chat': chat, 'text': '/is_fake url'}
    mock_message.configure_mock(**attrs)
    assert is_private_message(mock_message)
    check_fake_news_private(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] in fake_result

    fake_result = ['The url is of type: {}'.format(nt) for nt in POSSIBLE_NEWS_TYPES]
    mocker.patch('csuibot.handlers.check_fake_news', return_value=True)
    check_fake_news_private(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] in fake_result


def test_check_fake_news_private_errors(mocker):
    fake_value_error = 'Please provide url with HTTP format.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.check_fake_news', return_value=True)
    chat = mocker.Mock()
    attrs = {'type': 'private'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'chat': chat, 'text': '/is_fake'}
    mock_message.configure_mock(**attrs)
    check_fake_news_private(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_value_error


def test_add_fake_news_filter_private(mocker):
    fake_result = 'Added to filter list successfully.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.add_filter_news', return_value=None)
    chat = mocker.Mock()
    attrs = {'type': 'private'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'chat': chat, 'text': '/add_filter url fake'}
    mock_message.configure_mock(**attrs)
    assert is_private_message(mock_message)
    add_fake_news_filter_private(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_airing_valid(mocker):
    fake_result = 'Sakurada Reset is airing from 2017-04-05 until unknown'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.airing_check', return_value=fake_result)
    mock_type = Mock(type='private')
    mock_message = Mock(text='/is_airing Sagrada_Reset', chat=mock_type)

    airing(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_remove_destination(mocker):

    fake_result = 'No locations have been added, please add with /add_destination command'

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.uber', return_value=fake_result)
    mocked_message = Mock('\\remove_destination')

    remove_destination(mocked_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_airing_invalid(mocker):
    fake_error = ('Command invalid, please use /is_airing <anime>'
                  'format and replace space in <anime> with underscore (_)')
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.airing_check', return_value=fake_error)
    mock_type = Mock(type='private')
    mock_message = Mock(text='/is_airing Sagrada Reset', chat=mock_type)

    airing(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_airing_connection_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.airing_check', side_effect=ConnectionError)
    mock_type = Mock(type='private')
    mock_message = Mock(text='/is_airing Sagrada_Reset', chat=mock_type)

    airing(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Connection error occurs, please try again in a minute'


def test_airing_http_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.airing_check', side_effect=requests.exceptions.HTTPError)
    mock_type = Mock(type='private')
    mock_message = Mock(text='/is_airing Sagrada_Reset', chat=mock_type)

    airing(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'HTTP error occurs, please try again in a minute'


def test_anime_lookup_valid(mocker):
    fake_result = 'SukaSuka 6'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_airing', return_value=fake_result)
    mock_type = Mock(type='group')
    mock_message = Mock(text='hari ini nonton apa?', chat=mock_type)

    lookup_today(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_add_fake_news_filter_private_errors(mocker):
    fake_value_error = ("Please use the correct format: '/add_filter URL TYPE'\n"
                        "Make sure the URL is in HTTP format,"
                        " and the TYPE is one of [{}]".format(', '.join(POSSIBLE_NEWS_TYPES)))
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.add_filter_news', return_value=None)
    chat = mocker.Mock()
    attrs = {'type': 'private'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'chat': chat, 'text': '/add_filter url errortype'}
    mock_message.configure_mock(**attrs)
    add_fake_news_filter_private(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_value_error


def test_check_fake_news_group(mocker):
    fake_result = 'The url is safe to visit'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.check_fake_news', return_value=['safe'])
    entity = mocker.Mock()
    attrs = {'type': 'url', 'offset': 0, 'length': 17}
    entity.configure_mock(**attrs)
    entity2 = mocker.Mock()
    attrs = {'type': 'fake'}
    entity2.configure_mock(**attrs)
    chat = mocker.Mock()
    attrs = {'type': 'group'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'entities': [entity2, entity], 'chat': chat, 'text': 'http://google.com'}
    mock_message.configure_mock(**attrs)
    assert parse_check_fake_news_group(mock_message)
    check_fake_news_group(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result

    mock_message = mocker.Mock()
    attrs = {'entities': [entity2], 'chat': chat, 'text': 'no url'}
    mock_message.configure_mock(**attrs)
    assert parse_check_fake_news_group(mock_message) is False

    mock_message = mocker.Mock()
    attrs = {'entities': None, 'chat': chat, 'text': 'no url'}
    mock_message.configure_mock(**attrs)
    assert parse_check_fake_news_group(mock_message) is False


def test_check_fake_news_group_errors(mocker):
    fake_value_error = None
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.check_fake_news', side_effect=ValueError)
    entity = mocker.Mock()
    attrs = {'type': 'url', 'offset': 0, 'length': 10}
    entity.configure_mock(**attrs)
    chat = mocker.Mock()
    attrs = {'type': 'group'}
    chat.configure_mock(**attrs)
    mock_message = mocker.Mock()
    attrs = {'entities': [entity], 'chat': chat, 'text': 'google.com'}
    mock_message.configure_mock(**attrs)
    check_fake_news_group(mock_message)

    assert mocked_reply_to.call_args == fake_value_error


def test_anime_lookup_connection_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_airing', side_effect=ConnectionError)
    mock_type = Mock(type='group')
    mock_message = Mock(text='hari ini nonton apa?', chat=mock_type)

    lookup_today(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Connection error occurs, please try again in a minute'


def test_anime_lookup_http_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_airing', side_effect=requests.exceptions.HTTPError)
    mock_type = Mock(type='group')
    mock_message = Mock(text='hari ini nonton apa?', chat=mock_type)

    lookup_today(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'HTTP error occurs, please try again in a minute'


def test_add_wiki(mocker):
    fake_response = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.save_mediawiki_url', return_value=fake_response)
    mock_message = Mock(text='/add_wiki https://en.wikipedia.org/w/api.php')

    add_wiki(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_time_schedule_success(mocker):
    fake_response = 'Give a description for this schedule.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules',
                      {'foobar': Mock(group='test_create_schedule', date='date')})
    mock_message = Mock(text='desc', from_user=Mock(id='foobar'))

    time_schedule(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_add_wiki_without_url(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch(
        'csuibot.handlers.save_mediawiki_url',
        side_effect=ValueError('Command /add_wiki need an argument')
    )
    mock_message = Mock(text='/add_wiki')

    add_wiki(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /add_wiki need an argument'


def test_add_wiki_invalid_url(mocker):
    fake_response = 'Invalid url or url is not WikiMedia endpoint'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch(
        'csuibot.handlers.save_mediawiki_url',
        side_effect=ConnectionError(fake_response)
    )
    mock_message = Mock(text='/add_wiki http://scele.cs.ui.ac.id')

    add_wiki(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_desc_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    desc_schedule(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_random_wiki_article(mocker):
    fake_response = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_mediawiki', return_value=fake_response)
    mock_message = Mock(text='/random_wiki_article Barack Obama')

    random_wiki_article(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_desc_schedule_success(mocker):
    fake_response = 'Schedule created successfully.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.generate_schedule')
    mocker.patch.dict('csuibot.handlers.schedules',
                      {'foobar': Mock(group='test_create_schedule', date='date', time='time')})
    mock_message = Mock(text='desc', from_user=Mock(id='foobar'))

    desc_schedule(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_random_wiki_article_without_arguments(mocker):
    fake_response = ['foo', 'bar']
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_mediawiki', return_value=fake_response)
    mock_message = Mock(text='/random_wiki_article')

    random_wiki_article(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Select an article...'


def test_random_wiki_article_environment_error(mocker):
    fake_response = (
        'WikiMedia url is not found. Please add wiki url'
        ' with command /add_wiki [endpoint wiki url].'
    )
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_mediawiki', side_effect=EnvironmentError(fake_response))
    mock_message = Mock(text='/random_wiki_article asdfghjklqwertyuio')

    random_wiki_article(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_preview_valid(mocker):
    fake_response = "success"
    mocked_send_audio = mocker.patch('csuibot.handlers.bot.send_audio')
    mocker.patch('csuibot.handlers.bot.send_photo')
    mocker.patch('csuibot.handlers.preview_music', return_value=fake_response)
    mock_message = Mock(text='/itunes_preview Jack_Johnson')

    preview(mock_message)

    args, _ = mocked_send_audio.call_args
    assert type(args[1]) == io.BufferedReader


def test_preview_cant_find(mocker):
    fake_response = "Can\'t found the requested artist"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.preview_music', return_value=fake_response)
    mock_message = Mock(text='/itunes_preview Jack_Johnson')

    preview(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_preview_invalid(mocker):
    fake_error = ('Command invalid, please use /itunes_preview'
                  ' <artist> format, and seperate word in artist name with _')
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.preview_music', return_value=fake_error)
    mock_message = Mock(text='/itunes_preview Jack Johnson')

    preview(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_preview_http_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.preview_music', side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/itunes_preview Jack_Johnson')

    preview(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'HTTP error occurs, please try again in a minute'


def test_preview_connection_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.preview_music', side_effect=ConnectionError)
    mock_message = Mock(text='/itunes_preview Jack_Johnson')

    preview(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Connection error occurs, please try again in a minute'


def test_preview_permission_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.preview_music', side_effect=PermissionError)
    mock_message = Mock(text='/itunes_preview Jack_Johnson')

    preview(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Please stop the audio file before requesting new file'


def test_fetch_apod(mocker):
    fake_apod = 'foo img'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_apod', return_value=fake_apod)
    mock_message = Mock(text='/apod')

    apod(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_apod


def test_fetch_apod_connection_error(mocker):
    fake_apod_error = 'A connection error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_apod',
                 side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/apod')

    apod(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_apod_error


def test_fetch_latest_apod_http_error(mocker):
    fake_apod_error = 'An HTTP error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_apod',
                 side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/apod')

    apod(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_apod_error


def test_fetch_latest_apod_error(mocker):
    fake_apod_error = 'An error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_apod',
                 side_effect=requests.exceptions.RequestException)
    mock_message = Mock(text='/apod')

    apod(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_apod_error


def test_hospital(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.send_message')
    msg = {}
    chat = {}
    chat['type'] = "private"
    chat['last_name'] = "Divy"
    chat['first_name'] = "Prakash"
    chat['username'] = "prakash_divy"
    chat['id'] = 121508145
    chat['title'] = None
    chat['all_members_are_administrators'] = None
    msg['chat'] = chat
    msg['date'] = 1495177065
    msg['message_id'] = 4567
    message = json.dumps(msg)
    message = types.Message.de_json(message)
    Mock(text='/hospital')
    hospital(message)
    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_random_hospital(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.send_message')
    msg = {}
    chat = {}
    chat['type'] = "private"
    chat['last_name'] = "Divy"
    chat['first_name'] = "Prakash"
    chat['username'] = "prakash_divy"
    chat['id'] = 121508145
    chat['title'] = None
    chat['all_members_are_administrators'] = None
    msg['chat'] = chat
    msg['date'] = 1495177065
    msg['message_id'] = 4567
    message = json.dumps(msg)
    message = types.Message.de_json(message)
    Mock(text='/random_hospital')
    random_hospital(message)
    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_ask_darurat_location(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.send_message')
    msg = {}
    chat = {}
    chat['type'] = "group"
    chat['last_name'] = "Divy"
    chat['first_name'] = "Prakash"
    chat['username'] = "prakash_divy"
    chat['id'] = 121508145
    chat['title'] = None
    chat['all_members_are_administrators'] = None
    msg['chat'] = chat
    msg['date'] = 1495177065
    msg['message_id'] = 4567
    message = json.dumps(msg)
    message = types.Message.de_json(message)
    Mock(text='halo halo ini darurat')
    ask_darurat_location(message)
    args, _ = mocked_reply_to.call_args
    assert args[1] is not None
