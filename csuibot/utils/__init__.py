from csuibot.utils import zodiac as z, trivia as trv
import json
import re
from datetime import datetime as d


def lookup_zodiac(month, day):
    zodiacs = [
        z.Aries(),
        z.Taurus(),
        z.Gemini(),
        z.Cancer(),
        z.Leo(),
        z.Virgo(),
        z.Libra(),
        z.Scorpio(),
        z.Sagittarius(),
        z.Capricorn(),
        z.Aquarius(),
        z.Pisces()
    ]

    for zodiac in zodiacs:
        if zodiac.date_includes(month, day):
            return zodiac.name
    else:
        return 'Unknown zodiac'


def lookup_chinese_zodiac(year):
    num_zodiacs = 12
    zodiacs = {
        0: 'rat',
        1: 'buffalo',
        2: 'tiger',
        3: 'rabbit',
        4: 'dragon',
        5: 'snake',
        6: 'horse',
        7: 'goat',
        8: 'monkey'
    }
    ix = (year - 4) % num_zodiacs

    try:
        return zodiacs[ix]
    except KeyError:
        return 'Unknown zodiac'


def add_question_trivia(question):
    return trv.Trivia().add_question(question)

def set_answer_trivia(arrayOfAnswer):
    return trv.Trivia().set_answer(arrayOfAnswer)

def set_correct_answer_trivia(correctAns, question_id=None):
    return trv.Trivia().set_correct_answer(correctAns, question_id)

def get_question_trivia():
    trvi = trv.Trivia().read()
    return trvi.questions

def get_answer_trivia(question_id):
    trvi = trv.Trivia().read()
    question = [q for q in trvi.questions if q['question_id'] == int(question_id)]
    return question[0]['answer']

def change_answer_trivia(arrayOfQuestion):
    return trv.Trivia().change_answer(arrayOfQuestion)

def play_trivia_game(group_id):
    trvi = trv.Trivia().read()
    result = trvi.play_game(int(group_id))
    if(result == 'group already started the games'):
        return result
    trvi.write()
    question = request_question(int(group_id))
    return question

def request_question(group_id):
    trvi = trv.Trivia().read()
    question = trvi.req_question(int(group_id))
    return question


def get_current_question(group_id):
    trvi = trv.Trivia().read()
    game = [g for g in trvi.games if g['group_id'] == int(group_id)]
    question = [q for q in trvi.questions if q['question_id'] == int(game[0]['current_q'])]
    return question[0]


def judge_answer(sender, group_id, answer):
    trvi = trv.Trivia().read()
    result = trvi.try_guessing(sender, int(group_id), answer)
    trvi.write()
    return result


def stop_games(group_id):
    trvi = trv.Trivia().read()
    result = trvi.stop_game(int(group_id))
    trvi.write()
    return result


def get_leaderboard(group_id):
    trvi = trv.Trivia().read()
    players = trvi.show_leaderboard(int(group_id))
    res = "Leaderboard game barusan: \n"
    for idx, player in enumerate(players):
        player = players[idx]
        res = res + str(idx+1) + ". " + str(player['id']) + " dengan score " + str(player['score']) + "\n"
    trvi.write()
    return res

def req_next_question(group_id):
    trvi = trv.Trivia().read()
    games = [g for g in trvi.games if g['group_id'] == int(group_id)]
    if(len(games) == 0):
        return "group hasn't started the games"
    games[0]['current_q'] = (games[0]['current_q']+1) % len(trvi.questions)
    for player in trvi.players:
        if(player['group_id'] == group_id):
            player['guess_left'] = 3
    trvi.write()
    question = request_question(group_id)
    return question


