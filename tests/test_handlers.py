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


def test_oricon_books_invalid_date(mocker):
    fake_output = 'Requested date is invalid.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books weekly 2001-02-31')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_invalid_month(mocker):
    fake_output = 'Requested date is invalid.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books weekly 2001-13-31')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_invalid_year(mocker):
    fake_output = 'Requested date is invalid.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books weekly ASDF-02-31')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_not_weekly(mocker):
    fake_output = 'Oricon books command currently only supports weekly at this time.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books daily 2011-02-31')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_not_monday(mocker):
    fake_output = 'Oricon books command only accepts dates of Mondays.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books daily 2011-05-12')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_before_earliest(mocker):
    fake_output = "Oricon books' earliest record is on 2017-04-10."
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books daily 2011-05-12')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_oricon_books_after_latest(mocker):
    fake_output = "Oricon books' earliest record is on 2017-04-10."
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_oricon_books')
    mock_message = Mock(text='/oricon books daily 2011-05-12')

    oricon_books(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output
