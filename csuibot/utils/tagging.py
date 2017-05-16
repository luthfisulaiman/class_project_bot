import requests
from csuibot import config


class Tagging:

    TELEGRAM_GET_FILE_API = "https://api.telegram.org/bot{}/getFile?file_id={}"
    TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot{}/{}"
    IMAGGA_API = "https://api.imagga.com/v1/tagging?url={}"

    def __init__(self, file_url):
        self.photo_id = file_url

    def get_json_tag(self, i):
        return self.json['results'][0]['tags'][i]['tag']

    def get_json_confidence(self, i):
        return int(self.json['results'][0]['tags'][i]['confidence'])

    def get_top_five(self):
        msg = ''
        for i in range(4):
            msg += "Tag:{},Confidence:{}\n".format(self.get_json_tag(i),
                                                   self.get_json_confidence(i))
        msg += "Tag:{},Confidence:{}".format(self.get_json_tag(i),
                                             self.get_json_confidence(i))
        return msg

    def getTag(self):
        r = requests.get(self.IMAGGA_API.format(self.get_photo_url()),
                         auth=(config.IMAGGA_API_KEY, config.IMAGGA_API_SECRET))
        r.raise_for_status()
        self.json = r.json()
        res = self.get_top_five()
        return res

    def get_photo_url(self):
        r = requests.get(self.TELEGRAM_GET_FILE_API.format(config.TELEGRAM_BOT_TOKEN,
                                                           self.photo_id))
        r.raise_for_status()
        j = r.json()
        return self.TELEGRAM_FILE_URL.format(config.TELEGRAM_BOT_TOKEN,
                                             j['result']['file_path'])
