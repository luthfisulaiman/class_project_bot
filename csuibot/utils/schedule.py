from datetime import datetime, date, time
import json


class Schedule:

    def __init__(self):
        self.path_schedules = '../../schedules/'

    def create_schedule(self, chat_id, date, time):
        print("{} {} {}".format(chat_id, date_time))

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
                output.append("{} jam {}: {}"
                              .format(str_date,
                                      str_time,
                                      data['schedules'][str_date][str_time]))
            return output
        except FileNotFoundError:
            return []


if __name__ == '__main__':
    print(Schedule().get_schedules('tes'))
