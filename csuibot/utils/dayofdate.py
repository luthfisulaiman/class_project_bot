import datetime
import calendar


class dayofdate:
    def __init__(self):
        pass

    def dayoutput(year, month, day):
        try:
            dateans = datetime.date(year, month, day)
            return calendar.day_name[dateans.weekday()]
        except ValueError:
            return ('Incorrect use of dayofdate command. '
                    'Please write a valid date in the form of yyyy-mm-dd, '
                    'such as 2016-05-13')
