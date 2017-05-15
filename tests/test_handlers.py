from unittest.mock import Mock

from csuibot.handlers import (help, zodiac, shio, oricon_books)


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
