from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer as SS
import requests as r
from datetime import datetime
import re


class Books:

    def __init__(self):
        self.url = "http://www.oricon.co.jp/rank/ob/w/{}/"

    def get_top_10(self, date):
        try:
            valid_date = datetime.strptime(date, '%Y-%m-%d')
            if not (valid_date.strftime('%A') == 'Monday'):
                return 'Oricon books command only accepts dates of Mondays.'
            if (datetime(2017, 4, 10) > valid_date):
                return "Oricon books' earliest record is on 2017-04-10"
        except ValueError:
            return 'Requested date is invalid.'

        page = r.get(self.url.format(date))
        if page.status_code == 404:
            return "No chart is found on this date."
        strainer = SS(class_='box-rank-entry')
        entries = BS(page.content, 'html.parser', parse_only=strainer)
        output = ''
        count = 1
        for entry in entries.find_all(class_='box-rank-entry'):
            title = entry.find(class_="title").text
            author = entry.find(class_="name").text
            info = entry.find(class_="list").contents
            release = info[1].text.split()[-1]
            release = '-'.join(re.split(r'\D', release)[:-1])
            sales = re.search(r'[0-9,]+', info[3].text).group()
            line = "({}) {} - {} - {} - {}".format(count, title, author, release, sales)
            output += line + '\n'
            count += 1
        return output
