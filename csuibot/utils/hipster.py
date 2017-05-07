import requests

import json


class HipsterGenerator:

    def __init__(self):
        self.requester = HipsterRequester()

    def generate(self, nums):
        if(nums < 1 or nums > 99):
            raise ValueError("Value must be betweeen 1 to 99")

        params = {"paras": nums, "html": "false"}
        result = self.requester.make_request(params)
        return result['text']


class HipsterRequester:

    def __init__(self):
        self.url = "http://hipsterjesus.com/api/"

    def make_request(self, task):
        req = requests.get(self.url, params=task)
        return json.loads(req.content)
