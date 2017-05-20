from unittest.mock import Mock

from csuibot.handlers import (help, zodiac, shio, jadwal, create_schedule, date_schedule, time_schedule, desc_schedule)


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


def test_jadwal_no_schedule(mocker):
    fake_schedule = 'No future schedules are found.'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_schedules', return_value=[])
    mock_message = Mock(text='/jadwal', chat=Mock(id='foobar', type='group'))

    jadwal(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_schedule


def test_jadwal_with_schedule(mocker):
    fake_schedule = "2017-05-25 jam 09.00: Breakfast at Tiffany's."
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_schedules', return_value=["2017-05-25 jam 09.00: Breakfast at Tiffany's."])
    mock_message = Mock(text='/jadwal', chat=Mock(id='foobar'))

    jadwal(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_schedule


def test_create_schedule(mocker):
    fake_response = 'When should the schedule be created?'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mock_message = Mock(text='desc', chat=Mock(id='foobar'), from_user=Mock(id='foobar'))

    create_schedule(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_response


def test_date_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_invalid_date(mocker):
    fake_response = 'The requested date is invalid. Try again.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='9999-9999-9999')

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_past_date(mocker):
    fake_response = 'You cannot make a schedule for the past. Try again.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='2000-01-01')

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_unavailable_date(mocker):
    fake_response = "That date's full. Try another date or use /cancel to cancel."
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_available_schedules', return_value=[])
    mock_message = Mock(text='2017-05-25', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_date_schedule_success(mocker):
    fake_response = 'Here are the available hours for 2017-05-25.'
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.get_available_schedules', return_value=['foobar'])
    mock_message = Mock(text='2017-05-25', from_user=Mock(id='foobar'))

    date_schedule(mock_message)

    args, _ = mocked_send_message.call_args
    assert args[1] == fake_response


def test_time_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    time_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_time_schedule_success(mocker):
    fake_response = 'Give a description for this schedule.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules',
                      {'foobar': Mock(group='test_create_schedule', date='date')})
    mock_message = Mock(text='desc', from_user=Mock(id='foobar'))

    time_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_desc_schedule_cancel(mocker):
    fake_response = 'create_schedule canceled.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch.dict('csuibot.handlers.schedules', {'foobar': 'foobar'})
    mock_message = Mock(text='/cancel', from_user=Mock(id='foobar'))

    desc_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response


def test_desc_schedule_success(mocker):
    fake_response = 'Schedule created successfully.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocked_send_message = mocker.patch('csuibot.handlers.bot.send_message')
    mocker.patch('csuibot.handlers.generate_schedule')
    mocker.patch.dict('csuibot.handlers.schedules',
                      {'foobar': Mock(group='test_create_schedule', date='date', time='time')})
    mock_message = Mock(text='desc', from_user=Mock(id='foobar'))

    desc_schedule(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_response
