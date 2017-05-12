import requests
from unittest.mock import Mock
from csuibot.handlers import (help, zodiac, shio, is_palindrome, loremipsum,
                              colour, xkcd, yelkomputer, meme, hipsteripsum, ip,
                              password, password_16, custom_chuck_joke, define,
                              kelaskata, compute_binary, calculate,
                              compute_help, compute_not_binary, composer,
                              remind, isUp, sceleNoticeHandler, definisi, note,
                              dayofdate, invalid_dayofdate, empty_dayofdate,
                              marsfasilkom, yelfasilkom,
                              chuck, get_discrete_material as dm, message_dist,
                              oricon_cd)
from requests.exceptions import ConnectionError


def test_help(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock()

    help(mock_message)

    args, _ = mocked_reply_to.call_args
    expected_text = (
        'CSUIBot v0.0.3\n\n'
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


def test_message_dist(mocker):
    actual_dist = {'dist': {}}
    actual_dist['dist'][str(0)] = {}
    for i in range(0, 24):
        actual_dist['dist'][str(0)][str(i)] = 0
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_message_dist', return_value=actual_dist)
    mock_message = Mock(text='/message_dist')

    message_dist(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] is not None


def test_marsfasilkom(mocker):
    fake_marsfasilkom = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_marsfasilkom', return_value=fake_marsfasilkom)
    mock_message = Mock(text='/marsfasilkom')

    marsfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_marsfasilkom


def test_marsfasilkom_with_arguments(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_marsfasilkom', side_effect=ValueError)
    mock_message = Mock(text='/marsfasilkom some_arguments_here')

    marsfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /marsfasilkom doesn\'t need any arguments'


def test_yelfasilkom(mocker):
    fake_yelfasilkom = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelfasilkom', return_value=fake_yelfasilkom)
    mock_message = Mock(text='/yelfasilkom')

    yelfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_yelfasilkom


def test_yelfasilkom_with_arguments(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_yelfasilkom', side_effect=ValueError)
    mock_message = Mock(text='/yelfasilkom some_arguments_here')

    yelfasilkom(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /yelfasilkom doesn\'t need any arguments'


def test_discrete_number(mocker):
    test_noconnection = 'Cannot connect to API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=test_noconnection)
    mock_message = Mock(text='/tellme number theory')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == test_noconnection


def test_discrete_gcd(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme gcd')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_lcm(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme lcm')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_relasi_rekurensi(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme relasi rekurensi')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_relasi_biner(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme relasi biner')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_domain(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme domain')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_discrete_range(mocker):
    fake_discrete = ''
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_discrete_material', return_value=fake_discrete)
    mock_message = Mock(text='/tellme range')

    dm(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_discrete


def test_notes_view(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/notes view')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'No notes yet'


def test_notes_invalid_json_notes(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.manage_notes', return_value='Notes added')
    mock_message = Mock(text='/notes dasdsadassd')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Notes added'


def test_notes_file_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.manage_notes', side_effect=FileNotFoundError)
    mock_message = Mock(text='/notes view')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'No notes yet'


def test_notes_no_argument(mocker):
    fake_message = 'Usage :\n' + \
                   '1. /notes view : View note in this group\n' + \
                   '2. /notes [text] : Add new note in this group\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/notes')

    note(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_message


def test_definisi_connection_error(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_definisi', side_effect=requests.ConnectionError)
    mock_message = Mock(text='/definisi tralalala')

    definisi(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Oops! There was a problem. Maybe try again later :('


def test_definisi_help(mocker):
    fake_word = '/definisi [word] : return definition of' + \
                ' the word in indonesian language\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/definisi')

    definisi(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_word


def test_definisi(mocker):
    fake_definisi = 'Nomina:\n1. perahu; kapal\n\n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/definisi bahtera')

    definisi(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_definisi


def test_sceleNotif(mocker):
    fake_scele = 'scele'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.takeSceleNotif', return_value=fake_scele)
    mock_message = Mock(text='/sceleNotif')
    sceleNoticeHandler(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_scele


def test_is_up(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up https://scele.cs.ui.ac.id/')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'UP'


def test_is_down(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up http://iniwebsitedownwoi.co.id')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'DOWN'


def test_error_url(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_up ftp://example.com')

    isUp(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Url is invalid,insert a valid url!.Ex: https://www.google.com'


def test_remind_valid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 15 WakeUp')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'WakeUp'


def test_remind_valid_input_more(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 15 WakeUp Cmon')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'WakeUp Cmon'


def test_remind_more_than_thirty(mocker):

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/remindme 45 WakeUp')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Please input from range 0-29 only'


def test_remind_invalid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.remind_me', side_effect=ValueError)
    mock_message = Mock(text='/remindme sial sial')

    remind(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Invalid time input, only positive integer accepted.'


def test_compute_binary_valid_addtion(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 0011+0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '7'


def test_compute_binary_valid_subtraction(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1000-0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '4'


def test_compute_binary_valid_multiplication(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 0011*0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '12'


def test_compute_binary_valid_division(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1000/0100')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '2'


def test_compute_invalid_input(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 1234+12311')

    compute_not_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Not a binary number, Please only input binary number on both sides'


def test_compute_help(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute help')

    compute_help(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '''Binary Calculator v2.0, use /compute <binary><operand><binary>
to start a calculation.'''


def test_compute_invalid_operator(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=ValueError)
    mock_message = Mock(text='/compute 0101M0111')

    compute_binary(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == "Operator is invalid, please use '+', '-', '*', or '/'"


def test_define(mocker):
    fake_define = 'a precious stone consisting of a clear and colourless'
    fake_define += ' crystalline form of pure carbon,'
    fake_define += ' the hardest naturally occurring substance'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_define', return_value=fake_define)
    mock_message = Mock(text='/define diamond')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_define


def test_define_none_term(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_define', side_effect=ValueError)
    mock_message = Mock(text='/define')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Command /define need an argument'


def test_define_page_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.define', side_effect='404')
    mock_message = Mock(text='/define akugantengsekali')

    define(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '"akugantengsekali" is not an english word'


def test_kelaskata(mocker):
    fake_kata = 'intan/n'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', return_value=fake_kata)
    mock_message = Mock(text='/kelaskata intan')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_kata


def test_kelaskata_none_term(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=ValueError)
    mock_message = Mock(text='/kelaskata')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == 'Try /kelaskata [word]'


def test_kelaskata_word_not_found(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_kelaskata', side_effect=requests.ConnectionError)
    mock_message = Mock(text='/kelaskata akugantengsekali')

    kelaskata(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == '"akugantengsekali" is not a word'


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


def test_ip(mocker):
    fake_ip = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_public_ip', return_value=fake_ip)
    mock_message = Mock()

    ip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_ip


def test_ip_no_connection(mocker):
    fake_ip = 'Error connecting to ipify.org API, please try again later.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_public_ip', side_effect=ConnectionError)
    mock_message = Mock(text='/bot ip')

    ip(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_ip


def test_hipster_valid(mocker):
    fake_paragraph = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.make_hipster', return_value=fake_paragraph)
    mock_message = Mock(text='/hipsteripsum 3')

    hipsteripsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_paragraph


def test_hipster_paragraph(mocker):
    fake_paragraph = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.make_hipster', return_value=fake_paragraph)
    mock_message = Mock(text='/hipsteripsum 100')

    hipsteripsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_paragraph


def test_meme_valid(mocker):
    fake_meme = 'foo bar'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.get_meme', return_value=fake_meme)
    mock_message = Mock(text='/meme top bottom')

    meme(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_meme


def test_is_palindrome(mocker):
    fake_yes = 'Yes, it is a palindrome'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_palindrome tamat')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_yes


def test_is_not_palindrome(mocker):
    fake_no = 'No, it is not a palindrome'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/is_palindrome akhir')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_no


def test_error_is_palindrome(mocker):
    fake_error = 'You can only submit a word'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.is_palindrome', side_effect=ValueError)
    mock_message = Mock(text='/is_palindrome test 123 456 789')

    is_palindrome(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_lorem_ipsum(mocker):
    fake_loripsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                    'Proclivi currit oratio. ' \
                    'Honesta oratio, Socratica, Platonis etiam. ' \
                    'Aliter homines, aliter philosophos loqui putas oportere? ' \
                    'Quid ergo?'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_lorem_ipsum', return_value=fake_loripsum)
    mock_message = Mock(text='/loremipsum')

    loremipsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_loripsum


def test_lorem_ipsum_no_connection(mocker):
    fake_loripsum = 'Cannot connect to loripsum.net API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_lorem_ipsum', side_effect=ConnectionError)
    mock_message = Mock(text='/loremipsum')

    loremipsum(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_loripsum


def test_fetch_latest_xkcd(mocker):
    fake_xkcd = 'fake alt, fake img'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd', return_value=fake_xkcd)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd


def test_fetch_latest_xkcd_invalid(mocker):
    fake_xkcd_invalid = 'Command is invalid. You can only use "/xkcd" command.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd', side_effect=ValueError)
    mock_message = Mock(text='/xkcd 123123')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_invalid


def test_fetch_latest_xkcd_connection_error(mocker):
    fake_xkcd_error = 'A connection error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_fetch_latest_xkcd_http_error(mocker):
    fake_xkcd_error = 'An HTTP error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_fetch_latest_xkcd_error(mocker):
    fake_xkcd_error = 'An error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.fetch_latest_xkcd',
                 side_effect=requests.exceptions.RequestException)
    mock_message = Mock(text='/xkcd')

    xkcd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_xkcd_error


def test_colour(mocker):
    pure_red = 'RGB(255, 0, 0)'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/colour #ff0000')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == pure_red


def test_colour_invalid(mocker):
    rgb_invalid = 'Invalid command. Please use either /color #HEXSTR or /colour #HEXSTR'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/colour #123qwe')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == rgb_invalid


def test_colour_connection_error(mocker):
    fake_colour_error = 'A connection error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.ConnectionError)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


def test_colour_http_error(mocker):
    fake_colour_error = 'An HTTP error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.HTTPError)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


def test_colour_error(mocker):
    fake_colour_error = 'An error occured. Please try again in a moment.'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.convert_hex2rgb',
                 side_effect=requests.exceptions.RequestException)
    mock_message = Mock(text='/colour #123456')

    colour(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_colour_error


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


def test_composer(mocker):
    fake_track_info = 'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'iamlione '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'iamlione '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'iamlione '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'iamlione'\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'iamlione '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_composer', return_value=fake_track_info)
    mock_message = Mock(text='/sound_composer iamlione')

    composer(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_track_info


def test_composer_no_connection(mocker):
    fake_error = 'Error connecting to Soundcloud API'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.call_composer', side_effect=ConnectionError)
    mock_message = Mock(text='/sound_composer iamlione')

    composer(mock_message)
    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_compute_addition(mocker):
    fake_result = 7
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_substraction(mocker):
    fake_result = 3
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 10-7')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiplication(mocker):
    fake_result = 12
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4*3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division(mocker):
    fake_result = 10
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 30/3')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_multiple_operator(mocker):
    fake_result = 3
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 4+3-2*10/5')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_result


def test_compute_division_by_zero(mocker):
    fake_error = 'Cannot divide by zero'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=ZeroDivisionError)
    mock_message = Mock(text='/compute 3/0')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_compute_single_digit(mocker):
    fake_error = 12
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mock_message = Mock(text='/compute 12')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_error_compute(mocker):
    fake_error = 'Invalid command, please enter only numbers and operators'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.compute', side_effect=NameError)
    mock_message = Mock(text='/compute asdf')

    calculate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_dayofdate(mocker):
    fake_day = 'boink'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', return_value=fake_day)
    mock_message = Mock(text='/dayofdate 2016-05-13')

    dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_day


def test_dayofdate_invalid_command(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', side_effect=ValueError)
    mock_message = Mock(text='/dayofdate invalid')

    invalid_dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == ('Incorrect use of dayofdate command. '
                       'Please write a valid date in the form of yyyy-mm-dd, '
                       'such as 2016-05-13')


def test_dayofdate_no_argument(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.lookup_dayofdate', side_effect=ValueError)
    mock_message = Mock(text='/dayofdate')

    empty_dayofdate(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == ('Incorrect use of dayofdate command. '
                       'Please write a valid date in the form of yyyy-mm-dd, '
                       'such as 2016-05-13')


def test_chuck(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.chuck')
    mock_message = Mock(text='/chuck')

    chuck(mock_message)

    args, _ = mocked_reply_to.call_args
    assert "Chuck" in args[1]


def test_chuck_with_args(mocker):
    fake_error = 'Command /chuck doesn\'t need any arguments'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')
    mocker.patch('csuibot.handlers.chuck')
    mock_message = Mock(text='/chuck args')

    chuck(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_error


def test_top_oricon_cd_invalid_date(mocker):
    fake_output = 'Invalid date'
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles weekly 9999-99-99')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_top_oricon_cd_unknown(mocker):
    fake_output = "Oricon don't know chart in this date"
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles daily 1854-01-02')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output


def test_top_oricon_cd(mocker):
    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles weekly 2017-05-15')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert len(args[1].split('\n')) >= 10


def test_top_oricon_help(mocker):
    fake_output = ''

    mocked_reply_to = mocker.patch('csuibot.handlers.bot.reply_to')

    mock_message = Mock(text='/oricon jpsingles')

    oricon_cd(mock_message)

    args, _ = mocked_reply_to.call_args
    assert args[1] == fake_output
