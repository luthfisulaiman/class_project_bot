import json
import os

class Trivia:

    def __init__(self):
        self.path_trivia = os.path.abspath('csuibot/trivia.json')
        self.json = None
        self.question = None
        self.players = None
        self.games = None

    def read(self):
        with open(self.path_trivia) as file:
            self.json = json.load(file)
            self.questions = self.json['questions']
            self.players = self.json['players']
            self.games = self.json['games']
            return 'success'

    def write(self):
        with open(self.path_trivia, 'w') as file:
            self.json['games'] = self.games
            self.json['players'] = self.players
            self.json['question'] = self.questions
            json.dump(self.json, file, ensure_ascii=True)
            return json.dumps(self.json)
            

    def add_question(self, question):
        self.read()    
        question_id = len(self.questions)
        new_question = {'question_id': question_id, 'question': question, 'answer': [], 'correct': ""}
        self.questions.append(new_question)
        self.write()
        return 'success'

    def set_answer(self, answers) :
        self.read()
        question_id = len(self.questions)-1
        question = [q for q in self.questions if q['question_id'] == question_id]
        if(len(question) == 0):
            return "question not found"
        question[0]['answer'] = answer
        self.write()
        return "success"

    def set_correct_answer(self, correct_answer, question_id= None):
        self.read()
        if(question_id is None):
            question = [q for q in self.questions if q['correct'] == '']
            question_id = question[0]['question_id']
        question = [q for q in slef.questions if q['question_id'] == question_id]

        if(len(question) == 0):
            return "question not found"

        question[0]['correct'] = correct_answer
        self.write()

        ret = 'Pertanyaan : \'' + question[0]['question'] + "\" jawaban : "
        for answer in question[0]['answer']:
            if(answer == correct_answer):
                ret = ret + "*" + answer + "*"
            else:
                ret = ret + " " + answer
        return ret
        
    def play_game(self, group_id):
        game = [g for g in self.games if g['group_id'] == group_id]

        if(len(game) > 0):
            return "group already started the games"

        new_game = {'group_id': group_id, 'current_q': 0}
        self.games.append(new_game)
        return "success"

    def req_question(self, group_id):
        game = [g for g in self.games if g['group_id'] == group_id]

        if(len(game) == 0):
            return "group hasn't started the games"

        q_num = game[0]['current_q']

        for q in self.questions:
            if(q['question_id'] < q_num):
                continue
            if(len(q['answer']) > 0):
                game[0]['current_q'] = (q['question_id']+1) % len(self.questions)
                return q

        # havent found one, iterate from index
        ret = None
        for q in self.questions:
            if ret is not None:
                continue
            if(len(q['answer']) > 0):
                game[0]['current_q'] = (q['question_id']+1) % len(self.questions)
                ret = q

        return ret

    def can_answer(self, sender_id, group_id):
        player = [p for p in self.players if p['id'] == sender_id and p['group_id'] == group_id]

        return player[0]['guess_left'] > 0

    
    def guessing_true(self, sender_id, group_id):
        player = [p for p in self.players if p['id'] == sender_id and p['group_id'] == group_id]
        games = [g for g in self.games if g['group_id'] == group_id]

        player[0]['score'] = player[0]['score'] + 1
        games[0]['current_q'] = (games[0]['current_q']+1) % len(self.questions)
        for p in self.players:
            if(p['group_id'] == group_id):
                p['guess_left'] = 3

        return "success"

    def guessing_false(self, sender_id, group_id):
        player = [p for p in self.players if p['id'] == sender_id and p['group_id'] == group_id]

        player[0]['guess_left'] = player[0]['guess_left'] - 1
        return "success"

    def try_guessing(self, sender_id, group_id, answer):
        player = [p for p in self.players if p['id'] == sender_id and p['group_id'] == group_id]

        if len(player) == 0:
            new_player = {'id': sender_id, 'group_id': group_id, 'score': 0, 'guess_left': 3}
            self.players.append(new_player)

        if self.can_answer(sender_id, group_id) is False:
            return "kesempatan guess telah habis"

        games = [g for g in self.games if g['group_id'] == group_id]
        question = [q for q in self.questions if q['question_id'] == games[0]['current_q']]
        if(question[0]['correct'] == answer):
            self.guessing_true(sender_id, group_id)
            return "Nice job"

        self.guessing_false(sender_id, group_id)
        return "Sorry try again"

    def stop_game(self, group_id):
        games = [g for g in self.games if g['group_id'] == group_id]
        if len(games) == 0:
            return "Your group hasn't started the game"

        for idx, g in enumerate(self.games):
            if(g['group_id'] == group_id):
                del self.games[idx]

        return "game stopped"

    def show_leaderboard(self, group_id):
        res = []

        for idx, p in enumerate(self.players):
            if(p['group_id'] == group_id):
                res.append(p)

        for idx, p in enumerate(self.players):
            if(p['group_id'] == group_id):
                del self.players[idx]

        return res
