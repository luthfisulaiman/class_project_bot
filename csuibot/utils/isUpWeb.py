from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class IsUpWeb :
    def __init__(self, url):
        self._url = url

    def isUp(self) :
        req = Request(self._url)
        try:
            response = urlopen(req)
        except URLError as e:
            return 'DOWN'
        else:
            return 'UP'

