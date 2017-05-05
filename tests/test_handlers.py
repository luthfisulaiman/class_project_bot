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


def test_compute_addition(mocker):
    fake_result = '7'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_substraction(mocker):
    fake_result = '3'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 10-7')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiplication(mocker):
    fake_result = '12'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4*3')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division(mocker):
    fake_result = '3'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 30/3')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiple_operator(mocker):
    fake_result = '3'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3-2*10/5')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division_by_zero(mocker):
    fake_error = 'Cannot divide by zero'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=ZeroDivisionError)
    mock_message = Mock(text='/compute 3/0')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_error_compute(mocker):
    fake_error = 'Invalid command, please enter only numbers and operators'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=NameError)
    mock_message = Mock(text='/compute asdf')

    compute(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error
