import requests
from xml.etree import ElementTree as ET


class AiringChecking():

    def __init__():
        raise NotImplemented

    def check():
        raise NotImplemented

class AirToday():

    def __init__():
        raise NotImplemented

    def look():
        raise NotImplemented

class MALRequester():

    @staticmethod
    def make_request(anime):
        url = "https://myanimelist.net/api/anime/search.xml?q="
        en_anime = quote(anime, safe='')
        url = url + "{}".format(anime)
        task = {"username":"fiersome08", "password":"fiersome"}
        res = requests.get(url, params=task)
        return res.json()

print(MALRequester.make_request("gochiusa"))