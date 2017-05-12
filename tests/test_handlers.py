from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, air_quality

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


def test_aqi(mocker):
    fake_aqi = '75\nModerate\nAir quality is acceptable; however, for some pollutants' \
               ' there may be a moderate health concern for a very small number of ' \
               'people who are unusually sensitive to air pollution.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality', return_value=fake_aqi)
    mock_message = Mock(text='/aqi llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_aqi


def test_aqi_over_quota(mocker):
    fake_aqi = 'Over quota on aqicn.org, please try again later'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality', return_value=fake_aqi)
    mock_message = Mock(text='/aqi llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_aqi


def test_aqi_invalid_city(mocker):
    fake_aqi = 'City not found, please try again with a different city'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality', return_value=fake_aqi)
    mock_message = Mock(text='/aqi llanfairpwllgwyngyllgogerycawdadqwdqdqz')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_aqi


def test_aqi_invalid_key(mocker):
    fake_aqi = 'Invalid API key, please contact administrator'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality', return_value=fake_aqi)
    mock_message = Mock(text='/aqi llanfairpwllgwyngyllgogerycawdadqwdqdqz')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_aqi


def test_aqi_connection_error(mocker):
    fake_aqi = 'Unable to connect to aqicn.org, please try again later'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.air_quality', side_effect=ConnectionError)
    mock_message = Mock(text='/aqi llanfairpwllgwyngyllgogerycawdadqwdqdqz')

    air_quality(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_aqi
