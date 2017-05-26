#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class Acronym:

    def add_acronym(self, message):
        file = open('/app/csuibot/utils/acronym.json', 'r')
        data = json.load(file)
        acronym_dict = message
        if acronym_dict['singkatan'] in data:
            message = "Data is already in library!"
        else:
            print(acronym_dict['singkatan'])
            print(acronym_dict['acronym'])
            print("Enter else in add_acronym --> Acronym")
            data.append(acronym_dict['singkatan'])
            data[acronym_dict['singkatan']].append({"singkatan": acronym_dict['singkatan']})
            data[acronym_dict['singkatan']].append({"acronym": acronym_dict['acronym']})
            with open("/app/csuibot/utils/acronym.json", 'w') as file:
                data = json.dump(data, file)

            message = "{} - {} has been added!" \
                      .format(acronym_dict['singkatan'], acronym_dict['singkatan'])
            print(message)
        return message

    def update_acronym(self, message):
        file = open('/app/csuibot/utils/acronym.json', 'r')
        data = json.load(file)
        acronym_dict = message
        old_acronym = data[acronym_dict['singkatan']]['acronym']
        data[acronym_dict['singkatan']]['acronym'] = acronym_dict['acronym']
        with open("/app/csuibot/utils/acronym.json", 'w') as file:
                data = json.dump(data, file)

        message = "{} has been changed into {}!" \
                  .format(old_acronym, data[acronym_dict['singkatan']])
        return message

    def delete_acronym(message):
        file = open('/app/csuibot/utils/acronym.json', 'r')
        data = json.load(file)
        acronym_dict = message
        data.pop(acronym_dict['singkatan'], None)

        message = "{} has been removed".format(acronym_dict['singkatan'])
        return message
