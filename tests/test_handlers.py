from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, custom_chuck_joke, yelkomputer


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
