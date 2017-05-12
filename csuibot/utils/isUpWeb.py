from urllib.request import Request, urlopen
from urllib.error import URLError


class IsUpWeb:
    def __init__(self, url):
        self._url = url

    def isup(self):
        req = Request(self._url)
        try:
            urlopen(req)
        except URLError:
            return 'DOWN'
        else:
            return 'UP'
