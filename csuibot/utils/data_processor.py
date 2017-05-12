import json
import os
from csuibot.utils import plant
from random import randint


def fetch_data(name):
    data = fetch_all_data()
    ret = plant.Plant('', False, '')
    for p in data:
        if name.lower() in p.get('name').lower().split():
            ret.name = p.get('name')
            ret.is_poisonous = True
            ret.description = p.get('description')

    return ret


def fetch_all_data():
    data = []
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/data.json') as json_file:
        json_data = json.load(json_file)
        data = json_data

    return data['plants']


def fetch_user_input(user_input):

    if user_input.lower() == 'triviaplant':
        return send_trivia()
    elif 'askplant'in user_input.lower().split():
        inputs = user_input.lower().split()
        all_data = fetch_all_data()
        for tmp in inputs:
            for data in all_data:
                if tmp in data['name'].lower():
                    return "Yes, " + data['name'] + " is poisonous. It causes " + data['cause']

        return "No. It's not poisonous"


def send_trivia():
    data = fetch_all_data()
    rand = randint(0, len(data) - 1)
    p = data[rand]

    info = "Did you know? " + p['name'] + " is poisonous plant. It causes " + p['cause']
    return info
