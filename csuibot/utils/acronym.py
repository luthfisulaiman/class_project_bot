#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class Acronym:

    def getJSON(self):
        file = open('/app/csuibot/utils/acronym.json', 'r', encoding='UTF-8')
        data = json.load(file)
        return data

    def add_acronym(self, message):
        data = getJSON()
        acronym_dict = message
        if acronym_dict['singkatan'] in data:
            message = "Data is already in library!"
        else:
            data.append(acronym_dict['singkatan'])
            data[acronym_dict['singkatan']].append({"singkatan":acronym_dict['singkatan']})
            data[acronym_dict['singkatan']].append({"acronym":acronym_dict['acronym']})

            message = "{} - {} has been added!".format(acronym_dict['singkatan'], acronym_dict['singkatan'])
        return message


    def update_acronym(self, message):
        data = getJSON()
        acronym_dict = message
        old_acronym = data[acronym_dict['singkatan']]['acronym']
        data[acronym_dict['singkatan']]['acronym'] = acronym_dict['acronym']

        message = "{} has been changed into {}!".format(old_acronym, data[acronym_dict['singkatan']])
        return message


    def delete_acronym(message):
        data = getJSON()
        acronym_dict = message
        data.pop(acronym_dict['singkatan'], None)

        message = "{} has been removed".format(acronym_dict['singkatan'])
        return message
