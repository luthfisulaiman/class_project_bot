import requests
from urllib.parse import quote
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import time


def checkdate(function):
    def wrapper(*args, **kwargs):
        date = function(*args, **kwargs)
        if(date == "0000-00-00"):
            date = "unknown"
        return date
    return wrapper


class AnimeInfo:

    def __init__(self):
        self.schedule = {}
        self.currentAnime = []

    def set_info(self, anime):
        self.currentAnime = anime

    def get_anime_status(self):
        return self.currentAnime[0][7].text

    def get_anime_name(self):
        return self.currentAnime[0][1].text

    @checkdate
    def get_start_date(self):
        return self.currentAnime[0][8].text

    @checkdate
    def get_finish_date(self):
        return self.currentAnime[0][9].text

    def set_animeschedule(self, animelist):
        self.schedule = animelist

    def get_today_anime(self):
        today = time.strftime("%Y-%m-%d")
        today_animes = []
        for anime in self.schedule:
            if anime['date'] == today:
                today_animes.append(anime)
        return today_animes


class Requester:

    def __init__(self):
        self.malurl = "https://myanimelist.net/api/anime/search.xml?q="
        self.lcharturl = "https://www.livechart.me/spring-2017/tv"

    def lchart_crawling(self):
        res = requests.get(self.lcharturl)
        html_page = BeautifulSoup(res.content, 'html.parser')
        anime_div = html_page.find_all('article', class_='anime tv')
        animelist = []
        for div in anime_div:
            name = div.find('h3', class_='main-title').text
            date, _ = div.find('time', {'datetime': True})['datetime'].split('T')
            temp, _, _ = div.find('div', class_='episode-countdown').text.split(':')
            episode = temp[2:len(temp)]
            animelist.append({"name": name, "date": date, "episode": episode})
        return animelist

    def make_request(self, anime):
        en_anime = quote(anime, safe='')
        task = self.malurl + "{}".format(en_anime)
        res = requests.get(task, auth=("fiersome08", "fiersome"))
        return res


class AiringManager:

    def __init__(self):
        self.animecenter = AnimeInfo()
        self.requester = Requester()

    def request(self, anime):
        res = self.requester.make_request(anime)
        if res.status_code == 204:
            raise ValueError("Can\'t find the anime")
        self.animecenter.set_info(ET.fromstring(res.text))

    def get_date(self):
        status = self.animecenter.get_anime_status()
        name = self.animecenter.get_anime_name()
        sdate = self.animecenter.get_start_date()
        fdate = self.animecenter.get_finish_date()
        output = ""
        if status.lower() == "Finished Airing".lower():
            output = "{} has finished airing at {}".format(name, fdate)
        elif status.lower() == "Not yet aired".lower():
            output = "{} will air starting at {}".format(name, sdate)
        elif status.lower() == "Currently Airing".lower():
            output = "{} is airing from {} until {}".format(name, sdate, fdate)
        return output

    def get_today_anime(self):
        schedule = self.requester.lchart_crawling()
        self.animecenter.set_animeschedule(schedule)
        output = ''
        today_anime = self.animecenter.get_today_anime()
        for anime in today_anime:
            output += "{} {}\n".format(anime['name'], anime['episode'])
        return output
