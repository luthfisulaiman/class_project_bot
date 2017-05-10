#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class DiscreteMath:

    def get_discrete_material(self, query):
        file = open('csuibot/utils/response.json', 'r')
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

            message1 = 'Course: {}\n\n'.format(course)
            message2 = 'Terminology: {}\n\n'.format(termin)
            message3 = 'Definition: {}\n\n'.format(definition)
            message4 = 'Example: {}\n\n'.format(example)
            message5 = 'Reference: {}\n\n'.format(reference)
            message6 = 'Problem: {}\n'.format(problem)
            message = message1 + message2 + message3 + message4 + message5 + message6
        return message

    print("done")
