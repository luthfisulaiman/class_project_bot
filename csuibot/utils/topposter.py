import operator
import json
import os
from pathlib import Path


class TopPoster:

    def __init__(self, update):

        self.posters_data = []
        self.last_chat_id = ''

        self.read_json_posters()
        self.process_update(update)

    def read_json_posters(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/posters_data.json'
        check_file = Path(file_path)
        if check_file.is_file():
            with open(file_path) as input_file:
                try:
                    res = json.load(input_file)
                except ValueError:
                    pass
                else:
                    self.posters_data = res['posters']

    def process_update(self, update):
        poster_id = update.message.from_user.id
        chat_id = update.message.chat.id
        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name

        self.last_chat_id = chat_id
        self.posters_data.append({'id': poster_id, 'chat_id': chat_id,
                                  'first_name': first_name, 'last_name': last_name})

        self.save_json_posters()

    def save_json_posters(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/posters_data.json'
        with open(file_path, 'w') as output_file:
            data_to_dump = {'posters': self.posters_data}
            json.dump(data_to_dump, output_file)

    def get_name(self, user_id):
        name = ""
        for entry in self.posters_data:
            if str(entry['id']) == user_id:
                name = entry['first_name'] + " "
                name += entry['last_name']

        return name

    def get_group_chat_id_list(self):
        group_posters = set()

        for data in self.posters_data:
            if data['chat_id'] == self.last_chat_id:
                group_posters.add(data['chat_id'])

        return group_posters

    def count_posters(self):

        post_list = {}
        group_posters = self.get_group_chat_id_list()
        while group_posters:
            member = group_posters.pop()
            for index, entry in enumerate(self.posters_data):
                id_poster = self.posters_data[index]['id']
                chat_id = self.posters_data[index]['chat_id']
                if id_poster == member and chat_id == self.last_chat_id:
                    if str(member) in post_list:
                        post_list[str(member)] += 1
                    else:
                        post_list[str(member)] = 1

        sorted_list = sorted(post_list.items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = sorted_list[:5]

        message = 'Top 5 posters: \n'
        c = 0
        last_post_num = -1
        for entry in sorted_list:
            if entry[1] == 0:
                break

            c += 1
            if entry[1] == last_post_num:
                c -= 1

            message += str(c) + ". " + str(self.get_name(entry[0]))
            message += " (" + str(entry[1]) + " posts)\n"
            last_post_num = entry[1]

        return message
