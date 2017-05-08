#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class DiscreteMath:

    def get_discrete_material(self, query):
        # with open('/app/csuibot/utils/response.json') as data_file:
        #     data = json.load(data_file)
        file = open('/app/csuibot/utils/response.json', 'r')
        data = json.load(file)

        try:
            selected_data = data['terminologies'][query]
        except KeyError:
            message = \
                'Sorry, no knowledge about {}, please contact someone to add a new Knowledge'\
                .format(query)
            return message
        else:
            course = data['course']
            termin = query
            definition = selected_data['definition']
            example = selected_data['example']
            reference = selected_data['ref']
            problem = selected_data['problem']

            message1 = '<b>course:</b> {}\n'.format(course)
            message2 = 'terminology: {}\n'.format(termin)
            message3 = 'definition: {}\n'.format(definition)
            message4 = 'example: {}\n'.format(example)
            message5 = 'reference: {}\n'.format(reference)
            message6 = 'problem: {}\n'.format(problem)
            message = message1 + message2 + message3 + message4 + message5 + message6
        return message

    print("done")
