import json


def get_message_dist():
    try:
        with open('dist.txt') as file:
            dist_file = json.load(file)
    except IOError:
        dist_file = 'Failed to open file.'
    return dist_file

def add_message_to_dist(chat_id, hour):
    try:
        with open('dist.txt') as file:
            dist = json.load(file)
    except IOError:
        dist = {'dist': {}}
        with open('dist.txt', 'w') as new_file:
            json.dump(dist, new_file)

    if str(chat_id) not in dist['dist']:
        dist['dist'][str(chat_id)] = {}
        for i in range(0, 24):
            dist['dist'][str(chat_id)][str(i)] = 0

    dist['dist'][str(chat_id)][str(hour)] = dist['dist'][str(chat_id)][str(hour)] + 1

    with open('dist.txt', 'w') as file:
        json.dump(dist, file)
