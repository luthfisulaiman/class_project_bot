import requests

import json


class define:
    def __init__(self, word):
        self.app_id = 'f0d6d4d9'
        self.app_key = '1194193a908a3b2612852bd7bd5ad2c3'

        self.language = 'en'
        self.word_id = word
        self.url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.language
        self.url = self.url + '/' + self.word_id.lower()

    def getDefine(self):
        r = requests.get(self.url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        if(r.status_code == 404):
            return '"' + self.word_id + '" is not an english word'
        else:
            result = json.dumps(r.json()['results'][0]['lexicalEntries'][0]['entries'][0]
                                ['senses'][0]['definitions'][0])
            return result[1:-1]
