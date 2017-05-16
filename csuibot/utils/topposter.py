import operator
import json
import os


class TopPoster:

    def __init__(self):
        self.all_data = self.get_all_bot_updates()
        self.group_id = self.get_group_chat_id()
        self.group_members = self.get_all_members_id()

    def get_top_poster(self):
        post_list = {}
        grp = self.group_members
        while grp:
            member = grp.pop()
            for index, member_id in enumerate(self.all_data):
                x = self.all_data[index]['message']['from']['id']
                y = self.all_data[index]['message']['chat']['id']
                if x == member and y == self.group_id:
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

    def get_all_members_id(self):
        members = []
        for index, member_id in enumerate(self.all_data):
            if self.all_data[index]['message']['chat']['id'] == self.group_id:
                members.append(self.all_data[index]['message']['from']['id'])
        return set(members)

    def get_name(self, user_id):
        name = ""
        for entry in self.all_data:
            if str(entry['message']['from']['id']) == user_id:
                name = entry['message']['from']['first_name'] + " "
                name += entry['message']['from']['last_name']

        return name

    def get_group_chat_id(self):
        group_id = self.all_data[len(self.all_data)-1]['message']['chat']['id']
        return group_id

    def get_all_bot_updates(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + '/test.json') as input_file:
            res = json.load(input_file)
            res = res['result']
        return res
