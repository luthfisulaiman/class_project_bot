import requests
import re

class Xkcd2Generator(object):
    class Xkcd2Singleton(object):
        def __init__(self):
            pass

        def get_img(self, comic_id):
            if(re.search('/w', comic_id)):
                raise ValueError
            if(int(comic_id) < 1):
                raise ValueError

            json = ComicRequester.make_request(comic_id)
            return json['img']

    instance = None

    def __new__(cls):
        if not Xkcd2Generator.instance:
            Xkcd2Generator.instance = Xkcd2Generator.Xkcd2Singleton()
        return Xkcd2Generator.instance


class ComicRequester():

    @staticmethod
    def make_request(comic_id):
        url = 'http://xkcd.com/{}/info.0.json'.format(comic_id)
        req = requests.get(url)
        req.raise_for_status()
        return req.json()