from . import app, bot
from .utils import lookup_zodiac, lookup_chinese_zodiac, calculate_binary

@bot.message_handler(regexp=r'^/about$')
def help(message):
    app.logger.debug("'about' command detected")
    about_text = (
        'CSUIBot v0.0.1\n\n'
        'Dari Fasilkom, oleh Fasilkom, untuk Fasilkom!'
    )
    bot.reply_to(message, about_text)


@bot.message_handler(regexp=r'^/zodiac \d{4}\-\d{2}\-\d{2}$')
def zodiac(message):
    app.logger.debug("'zodiac' command detected")
    _, date_str = message.text.split(' ')
    _, month, day = parse_date(date_str)
    app.logger.debug('month = {}, day = {}'.format(month, day))

    try:
        zodiac = lookup_zodiac(month, day)
    except ValueError:
        bot.reply_to(message, 'Month or day is invalid')
    else:
        bot.reply_to(message, zodiac)


@bot.message_handler(regexp=r'^/shio \d{4}\-\d{2}\-\d{2}$')
def shio(message):
    app.logger.debug("'shio' command detected")
    _, date_str = message.text.split(' ')
    year, _, _ = parse_date(date_str)
    app.logger.debug('year = {}'.format(year))

    try:
        zodiac = lookup_chinese_zodiac(year)
    except ValueError:
        bot.reply_to(message, 'Year is invalid')
    else:
        bot.reply_to(message, zodiac)


def parse_date(text):
    return tuple(map(int, text.split('-')))

@bot.message_handler(regexp=r'^\/compute ([^01]+[\/\+\-\*]+[^01]+)$')
def compute_not_binary(message):
    bot.reply_to(message, 'Not a binary number, Please only input binary number on both sides')

@bot.message_handler(regexp=r'^\/compute help$')
def compute_help(message):
    bot.reply_to(message, 'Binary Calculator v2.0, use /compute <binary><operand><binary> to start a calculation.')

@bot.message_handler(regexp=r'^\/compute ([01]+(.*)[01]+)$')
def compute(message):
    app.logger.debug("'compute' command detected")
    _, calculate_str = message.text.split(' ')
    try :
        if '+' in calculate_str:
            binA, binB = calculate_str.split('+')
            op = '+'
        elif '-' in calculate_str:
            binA, binB = calculate_str.split('-')
            op = '-'
        elif '*' in calculate_str:
            binA, binB = calculate_str.split('*')
            op = '*'
        elif '/' in calculate_str:
            binA, binB = calculate_str.split('/')
            op = '/'
        else :
            raise ValueError
    except ValueError:
        bot.reply_to(message, "Operator is invalid, please use '+', '-', '*', or '/'")
    else:
        result = calculate_binary(binA, op, binB)
        bot.reply_to(message, result)
            
         
    















