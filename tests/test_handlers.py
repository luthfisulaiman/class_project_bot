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
