from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, compute


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

def test_compute_binary_valid_addtion(mocker) :
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.calculate_binary', return_value = '7')
    mock_message = Mock(text='/compute 0011+0100')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '7'
def test_compute_binary_valid_subtraction(mocker) :
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.calculate_binary', return_value = '4')
    mock_message = Mock(text='/compute 1000-0100')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '4'
def test_compute_binary_valid_multiplication(mocker) :
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.calculate_binary', return_value = '12')
    mock_message = Mock(text='/compute 0011*0100')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '12'
def test_compute_binary_valid_division(mocker) :
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.calculate_binary', return_value = '2')
    mock_message = Mock(text='/compute 1000/0100')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '2'
    
def test_compute_invalid_input(mocker) :
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.calculate_binary', side_effect=ValueError)
    mock_message = Mock(text='/compute 1234+12311')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Not a binary number or operator is invalid!'
    
