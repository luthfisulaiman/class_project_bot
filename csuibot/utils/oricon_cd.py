from bs4 import BeautifulSoup as Bs
from bs4 import SoupStrainer as Ss
import requests as r
from requests.exceptions import ConnectionError
import datetime
import re


class Oricon_cd:
    ORICON_URL = "http://www.oricon.co.jp/rank/js/{}/{}/"

    @classmethod
    def get_top_ten(cls, chart_type, date):
        error_text = 'Invalid date'
        need_check = ['m', 'd', 'w']

        # check for date format
        regex = re.compile(r'(\d{4}|\d{4}-\d{2}|\d{4}-\d{2}-\d{2})')
        if regex.fullmatch(date) is None:
            return error_text

        if chart_type in need_check:
            month = date.split('-')[1]
            month = int(month.lstrip('0'))
            if month < 1 or month > 12:
                return error_text
            if chart_type != 'm':
                date_split = date.split('-')
                try:
                    datetime.date(int(date_split[0]),
                                  int(date_split[1].split('0')[-1]),
                                  int(date_split[2].split('0')[-1]))
                except ValueError:
                    return error_text
        try:
            page = cls._get_page(cls.ORICON_URL.format(chart_type, date))
        except ConnectionError:
            return 'Error occured when connecting to Oricon website.'

        if page.status_code == 404:
            return "Oricon don't know chart in this date"
        soup = cls.__parse_scraping_text(page.content)
        return cls.__get_output(soup)

    @classmethod
    def _get_page(cls, link):
        page = r.get(link)
        return page

    @classmethod
    def __parse_scraping_text(cls, html):
        strainer = Ss(class_='box-rank-entry')
        parse_html_text = Bs(html, 'html.parser', parse_only=strainer)
        return parse_html_text

    @classmethod
    def __get_output(cls, soup):
        output = ''
        for entry in soup.find_all(class_='box-rank-entry'):
            info = entry.find(class_="title").text
            info += ' - ' + entry.find(class_="name").text

            entry_info = entry.find(class_="list").contents
            release_date = entry_info[1].text.split()[-1]
            release_date = '-'.join(re.split(r'\D', release_date)[:-1])

            info += ' - ' + release_date

            sales = "No estimated sales"
            if len(entry_info) > 5:
                sales = re.search(r'[0-9,]+', entry_info[3].text).group()
            info += ' - ' + sales
            output += info + '\n'
        return output
