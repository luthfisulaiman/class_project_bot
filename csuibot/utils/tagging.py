import requests

class Tagging:

    def __init__(self, file_url):
        self.payload = {'api_key': '<example_api_key>'}
        self.url = "http://api.imagga.com/draft/tags"
        self.file = file_url

    def getTag(self):
        pass
