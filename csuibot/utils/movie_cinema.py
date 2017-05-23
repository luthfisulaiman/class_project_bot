import abc
from bs4 import BeautifulSoup as bs
import requests


class Movie_Cinema(metaclass=abc.ABCMeta):

    def __init__(self):
        self.BASE_URL = "https://www.cgv.id/en/schedule/cinema/0200"
        self.cinema_id = self.BASE_URL[-4:]

    def get_base(self):
        return self.BASE_URL

    def get_cinema_id(self):
        return self.cinema_id

    def set_base(self, new_url):
        self.BASE_URL = new_url

    def template_find_method(self, vals):
        return self.find_movies(vals)

    def template_change_method(self, url):
        return self.change_cinema(url)

    def find_movies(self, vals):
        pass

    def change_cinema(self, url):
        pass


class Concrete_Cinema(Movie_Cinema):

    def find_movies(self, vals):
        req = requests.get(self.BASE_URL).text
        try:
            soup = bs(req, "html.parser")
            result = temp_result = ""

            print()
            cinema = soup.find_all(id=self.cinema_id)
            for s_c in cinema:
                result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

            sched = soup.find_all(class_='schedule-type')
            for stype in sched:
                if vals in stype.text.lower():
                    temp_showtime = stype.findNext('ul').text.split('\n')
                    movie = stype.findNext('a')['movietitle']
                    temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
                    result += temp_result + "\n"

            if len(temp_result) == 0:
                return "There is no schedule"
            else:
                return result
        except:
            return 'error retrieving'

    def change_cinema(self, nurl):
        req = requests.get(self.BASE_URL)
        base = "/schedule/cinema/"

        try:
            soup = bs(req.text, "html.parser")
            sched = soup.find_all(class_='schedule-type')

            result = ""

            if base not in nurl or req.status_code == '404':
                return "invalid url"
            elif len(sched) == 0 or sched is None:
                return "cinema does not exist"
            else:
                self.set_base(nurl)
                result += "Cinema has changed successfully"
                return result
        except:
            return 'error retrieving'
