import requests

from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, yelkomputer, colour, xkcd


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
