import requests
import os.path
import json


class FakeNews:
    JSON_URL = ("https://raw.githubusercontent.com/BigMcLargeHuge"
                "/opensources/master/sources/sources.json")
    JSON_FILE_LOC = (".sources_cache.json")
    json = None

    def __init__(self):
        self.__load_json()

    def __save_json(self):
        with open(self.json_file, 'w') as json_file:
            json.dump(self.json, json_file)

    def __load_json(self):
        if self.json is None:
            if os.path.isfile(self.JSON_FILE_LOC):
                with open(self.JSON_FILE_LOC, 'r') as json_file:
                    self.json = json.load(json_file)
            else:
                r = requests.get(self.JSON_URL)
                self.json = r.json()
                self.__save_json()

    def check(self, hostname):
        if hostname in self.json:
            return self.json[hostname]
        return {'type': 'safe'}

    def add_filter(self, hostname, news_type):
        if hostname in self.json:
            json_element = self.json[hostname]
            if json_element['2nd type'] == "":
                json_element['2nd type'] = news_type
            else:
                json_element['3rd type'] = news_type
            self.json[hostname] = json_element
        else:
            json_element = {
                "type": news_type,
                "2nd type": "",
                "3rd type": "",
                "Source Notes (things to know?)": ""}
            self.json[hostname] = json_element
        self.__save_json()
