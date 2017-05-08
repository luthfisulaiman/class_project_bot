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

            message = 'course: {}\n terminology: {}\n definition: {}\n example: {}\n reference: {}\n \
                      problem: {}\n'\
                      .format(course, termin, definition, example, reference, problem)
        return message

    print("done")