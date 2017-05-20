from datetime import datetime, date, time
import json


class Schedule:
    class __Schedule:
        def __init__(self):
            self.path_schedules = 'schedules/'
    instance = None

    def __init__(self):
        if not Schedule.instance:
            Schedule.instance = Schedule.__Schedule()

    def __getattr__(self, name):
        return getattr(self.instance, name)


    def create_schedule(self, chat_id, req_date, req_time, req_desc):
        try:
            with open(self.path_schedules + str(chat_id) + '.json', 'r') as data_json:
                data = json.load(data_json)
        except IOError:
            data = {}
            data['schedules'] = {}
            data['schedules'][req_date] = {}

        data['schedules'][req_date][req_time] = req_desc

        with open(self.path_schedules + str(chat_id) + '.json', 'w') as file_json:
            json.dump(data, file_json)

    def get_available_schedules(self, chat_id, req_date):
        hours = ['09', '10', '11', '12', '13', '14']
        try:
            with open(self.path_schedules + str(chat_id) + '.json', 'r') as data_json:
                data = json.load(data_json)

            return list(set(hours) - data['schedules'][req_date].keys())
        except IOError:
            return hours
        except KeyError:
            return hours

    def get_schedules(self, chat_id):
        try:
            with open(self.path_schedules + str(chat_id) + '.json', 'r') as data_json:
                data = json.load(data_json)

            current_date = datetime.now().date()
            current_time = datetime.now().time()
            datetimes = []
            output = []

            for str_date, value in data['schedules'].items():
                y, m, d = str_date.split('-')
                the_date = date(int(y), int(m), int(d))
                if the_date >= current_date:
                    for str_time in value.keys():
                        the_time = time(int(str_time))
                        if the_date > current_date or (the_date == current_date and
                                                       the_time >= current_time):
                            datetimes.append(datetime.combine(the_date, the_time))
            datetimes.sort()
            for the_datetime in datetimes:
                str_date = the_datetime.strftime("%Y-%m-%d")
                str_time = the_datetime.strftime("%H")
                output.append("{} jam {}.00: {}"
                              .format(str_date,
                                      str_time,
                                      data['schedules'][str_date][str_time]))
            return output
        except IOError:
            return []
