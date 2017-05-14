import requests

from unittest.mock import Mock
from csuibot.handlers import (help, zodiac, shio, is_palindrome, loremipsum,
                              colour, xkcd, yelkomputer, meme, hipsteripsum, ip,
                              password, password_16, custom_chuck_joke, define,
                              kelaskata, hotcountry, newage, billArtist)
from requests.exceptions import ConnectionError


def test_help(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock()

    help(mock_message)

    args, _ = mocked_reply_to.call_args
    expected_text = (
        'CSUIBot v0.0.1\n\n'
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


def test_kelaskata(mocker):
    fake_kata = 'intan/n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', return_value=fake_kata)
    mock_message = Mock(text='/kelaskata intan')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_kata


def test_kelaskata_none_term(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=ValueError)
    mock_message = Mock(text='/kelaskata')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Try /kelaskata [word]'


def test_kelaskata_word_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=requests.ConnectionError)
    mock_message = Mock(text='/kelaskata akugantengsekali')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '"akugantengsekali" is not a word'


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
    mock_message = Mock(text='/xkcd 123123')

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


def test_hotcountry(mocker):
    fake_hotcountry = 'foobar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_hotcountry', return_value=fake_hotcountry)
    mock_message = Mock(text='/billboard hotcountry')

    hotcountry(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_hotcountry


def test_hotcountry_no_connection(mocker):
    fake_hotcountry = 'Cannot connect to billboard API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_hotcountry', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard hotcountry')

    hotcountry(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_hotcountry


def test_newage(mocker):
    fake_newage = 'foobar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_newage', return_value=fake_newage)
    mock_message = Mock(text='/billboard newage')

    newage(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_newage


def test_newage_no_connection(mocker):
    fake_newage = 'Cannot connect to billboard API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_newage', side_effect=ConnectionError)
    mock_message = Mock(text='/billboard newage')

    newage(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_newage


def test_billArtist_Pentatonix(mocker):
    fake_billArtist = "Pentatonix \n PTX Vol. IV: Classics (EP) \n Rank #93"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_billArtist', return_value=fake_billArtist)
    mock_message = Mock(text='/billboard bill200 Pentatonix')

    billArtist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_billArtist


def test_billArtist_not_exist(mocker):
    fake_billArtist = "Rhoma Irama doesn't exist in bill200"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_billArtist', side_effect=fake_billArtist)
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
