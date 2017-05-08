#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class DiscreteMath:

    def get_discrete_material(query):
        with open('/app/csuibot/utils/discretemath.json') as data_file:
            data = json.load(data_file)

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

            message = 'course: {} terminology: {} definition: {} example: {} reference: {} \
                      problem: {}'\
                      .format(course, termin, definition, example, reference, problem)
        return message

    print("done")
