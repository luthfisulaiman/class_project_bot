import requests


class FakeJson:

    def __init__(self):
        self._url = 'http://jsonplaceholder.typicode.com/posts/1'

    def get_response(self):
        return requests.get(self._url).text
