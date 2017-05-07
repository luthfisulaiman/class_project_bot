from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, define, kelaskata

import requests


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
