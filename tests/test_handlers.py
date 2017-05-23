from unittest.mock import Mock

from csuibot.handlers import help, zodiac, shio, enterkomputer


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


def test_enterkomputer(mocker):
    fake_result = 'DJI OSMO - Rp 6,990,000\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Drone DJI OSMO')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_enterkomputer_multi_item(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Mouse Logitech')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1]


def test_enterkomputer_no_category(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Nendoroid Nendoroid Megumi Kato')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Category Not Found'


def test_enterkomputer_no_item(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text='/enterkomputer Processor aqwesqeq')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Item Not Found'


def test_enterkomputer_insufficient_args(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.enterkomputer')
    mock_message = Mock(text = '/enterkomputer')

    enterkomputer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == "Not enough arguments, please provide category and item name with the format /enterkomputer CATEGORY ITEM"
