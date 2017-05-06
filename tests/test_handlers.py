from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, password, password_16


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
