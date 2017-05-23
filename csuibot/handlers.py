from . import app, bot, dictionary
from .utils import (lookup_zodiac, lookup_chinese_zodiac, add_question_trivia,
                    set_answer_trivia, set_correct_answer_trivia,
                    get_question_trivia, get_answer_trivia, change_answer_trivia,
                    play_trivia_game, request_question, get_current_question,
                    judge_answer, stop_games, get_leaderboard, req_next_question)
import validators
import datetime
from request.exception import ConnectionError
from telebot import types

def message_decorate(func):
    def func_wrap(message):
        now = datetime.datetime.now()
        # heroku's time differ with wib
        hour = (now.hour + 7) % 24
        sender = message.chat.id
        write_log(sender, hour)
        return func(message)
    return func_wrap


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


@bot.message_handler(regexp=r'^/add_question$')
@message_decorate
def add_question(message):
    app.logger.debug("'Add trivia question' command detected")
    msg = bot.reply_to(message, "Write your question!!!")
    bot.register_next_step_handler(msg, set_question)


def set_question(message):
    app.logger.debug("set question")
    question = message.text
    add_question_trivia(question)
    msg = bot.reply_to(message, "Write 4 answers seperated by newline")
    bot.register_next_step_handler(msg, set_answer)
    
    
def set_answer(message):
    app.logger.debug("'setting answer' command detected")
    answer = message.text
    answer_set = answer.split("\n")
    set_answer_trivia(answer_set)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(answer_set[0])
    button2 = types.KeyboardButton(answer_set[1])
    button3 = types.KeyboardButton(answer_set[2])
    button4 = types.KeyboardButton(answer_set[3])
    markup.add(button1, button2, button3, button4)
    msg = bot.reply_to(message, "Choose correct answer:", reply_markup=markup)
    bot.register_next_step_handler(msg, set_correct_answer)

def set_correct_answer(message):
    app.logger.debug("set answer command detected")
    correct = message.text
    result = set_correct_answer_trivia(correct)
    bot.reply_to(message, result, parse_mode='Markdown')


@bot.message_handler(regexp=r'^/change_answer$')
def change_answer(message):
    app.logger.debug("'Change answer' command detected")
    question_set = get_question()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    for q in question_set:
        button = types.KeyboardButton(str(q['question_id'] + ". " + q['question']))
        markup.add(button)
    msg = bot.reply_to(message, "Choose question to change answer", reply_markup = markup)
    bot.register_next_step_handler(msg, change_answer_next)

def change_answer_next(message):
    app.logger.debug('change answer next detected')
    question_id, _ = message.text.split(".")
    answer_set = get_answer_trivia(question_id)
    delete_previous_correct_trivia(question_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    for a in answer_set:
        button = types.KeyboardButton(a)
        markup.add(button)
    msg = bot.reply_to(message, "Choose correct answer:", reply_markup=markup)
    bot.register_next_step_handler(msg, set_correct_answer)
    
@bot.message_handler(regexp=r'^start zonk$')
@message_decorate
def start_zonk(message):
    app.logger.debug("'start zonk' command detected")

    if message.chat.type == 'private':
        bot.reply_to(message, 'Perintah ini hanya bisa di group chat')
        return

    group_id = message.chat.id
    question = play_trivia_game(group_id)
    if(question == 'group already started the games'):
        bot.reply_to(message, question)
    else:
        res = question['question'] + "\n"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        for a in question['answer']:
            button = types.KeyboardButton(a)
            markup.add(button)
        msg = bot.reply_to(message, res, reply_markup=markup)
        bot.register_next_step_handler(msg, try_answer)

def try_answer(message):
    app.logger.debug('try answer')
    answer = message.text
    sender = message.from_user.username
    group_id = message.chat.id
    if(answer == "start zonk" or answer == "stop zonk" or answer == "next question"):
        bot.reply_to(message, "")
        return
    result = judge_answer(sender, group_id, answer)
    if result == "kesempatan guess telah habis":
        bot.reply_to(message, result)
        return
    if result == "Sorry try again":
        question = get_current_question(group_id)
        res = "Sorry jawaban anda salah " + ","
        res = res + question['question'] + "\n"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        for a in question['answer']:
            itembtn = types.KeyboardButton(a)
            markup.add(itembtn)
        msg = bot.reply_to(message, res, reply_markup=markup)
        bot.register_next_step_handler(msg, try_answer)
    if result == "Nice job":
        question = req_question(group_id)
        res = "Selamat jawaban anda benar " + ","
        res = res + question['question'] + "\n"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        for a in question['answer']:
            itembtn = types.KeyboardButton(a)
            markup.add(itembtn)
        msg = bot.reply_to(message, res, reply_markup=markup)
        bot.register_next_step_handler(msg, try_answer)

@bot.message_handler(regexp=r'^next question$')
@message_decorate
def next_question(message):
    app.logger.debug("next question")

    if message.chat.type == 'private':
        bot.reply_to(message, 'Perintah ini hanya bisa di group chat.')
        return

    group_id = message.chat.id
    question = req_next_question(group_id)
    res = "Skip soal. Soal selanjutnya " + ","
    res = res + question['question'] + "\n"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    for a in question['answer']:
        itembtn = types.KeyboardButton(a)
        markup.add(itembtn)
    msg = bot.reply_to(message, res, reply_markup=markup)
    bot.register_next_step_handler(msg, try_answer)

