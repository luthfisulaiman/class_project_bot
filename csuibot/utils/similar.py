import requests
from urllib.parse import quote
from os import environ


def checkconnection(function):
    def wrapper(*args, **kwargs):
        for arg in args:
            if(isinstance(arg, str)):
                res = requests.head(arg)
                res.raise_for_status()
        return function(*args, **kwargs)
    return wrapper


def checktext(function):
    def wrapper(*args, **kwargs):
        for arg in args:
            if(isinstance(arg, str)):
                if(len(arg) >= 500):
                    raise ValueError
        return function(*args, **kwargs)
    return wrapper


class SimilarText:

    def __init__(self):
        self.requester = ApiRequester()

    @checktext
    def checktext(self, text1, text2):
        res = self.requester.make_request_text(text1, text2)
        return  "similarity:" + str(float(res['langConfidence']) * 100) + "%"

    @checkconnection
    def checkweb(self, url1, url2):
        res = self.requester.make_request_url(url1, url2)
        return "similarity:" + str(float(res['langConfidence']) * 100) + "%"


class ApiRequester:

    def __init__(self):
        self.url = 'https://api.dandelion.eu/datatxt/sim/v1'
        self.auth = environ.get('DANDELION_KEY')

    def make_request_text(self, text1, text2):
        en_text1 = quote(text1, safe='')
        en_text2 = quote(text2, safe='')
        task = self.url + "/?text1={} &text2={}&token={}".format(en_text1, en_text2, self.auth)
        req = requests.get(task)
        req.raise_for_status()
        return req.json()

    def make_request_url(self, url1, url2):
        en_url1 = quote(url1, safe='')
        en_url2 = quote(url2, safe='')
        task = self.url + "/?url1={} &url2={}&token={}".format(en_url1, en_url2, self.auth)
        req = requests.get(task)
        req.raise_for_status()
        return req.json()
