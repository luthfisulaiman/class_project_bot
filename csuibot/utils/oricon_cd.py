from bs4 import BeautifulSoup as Bs
from bs4 import SoupStrainer as Ss
import requests as r
from requests.exceptions import ConnectionError


class Oricon_cd:
    ORICON_URL = "http://www.oricon.co.jp/rank/js/{}/{}"

    @classmethod
    def get_top_ten(cls, chart_type, date):
        if chart_type == 'y':
            
        elif chart_type == 'm':

        elif chart_type == 'w':

        elif chart_type == 'd':

        else:
                

    @classmethod
    def __get_page(cls, link):
        page = requests.get(link)
        return page.content

    @classmethod
    def __parse_scraping_text(cls, html):
        strainer = SoupStrainer(class_='box-rank-entry')
        parse_html_text = BeautifulSoup(html, 'html.parser', parse_only=strainer)
        return parse_html_text
