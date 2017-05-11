import requests
from csuibot import config, app


class ExtractColour:

    TELEGRAM_GET_FILE_API = "https://api.telegram.org/bot{}/getFile?file_id={}"
    TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot{}/{}"
    IMAGGA_API = "https://api.imagga.com/v1/colors?url={}"
    FGCOLOUR, BGCOLOUR = ("FGCOLOUR", "BGCOLOUR")  # caption to choose extract method

    def __init__(self, photo_id):
        app.logger.debug('create ExtractColour, photo_id:{}'.format(photo_id))
        self.photo_id = photo_id

    @property
    def state(self):
        return (ExtractColour.FGCOLOUR if self.__extract_method == self.__extract_fgcolour
                else ExtractColour.BGCOLOUR)

    @state.setter
    def state(self, state):
        if state == ExtractColour.FGCOLOUR:
            self.__extract_method = self.__extract_fgcolour
        else:
            self.__extract_method = self.__extract_bgcolour

    def extract(self):
        app.logger.debug('ExtractColour, call extract()')
        r = requests.get(self.IMAGGA_API.format(self.get_photo_url()),
                         auth=(config.IMAGGA_API_KEY, config.IMAGGA_API_SECRET))
        r.raise_for_status()
        self.json = r.json()
        app.logger.debug('ExtractColour extract(), json:{}'.format(self.json))
        extracted = self.__extract_method()
        app.logger.debug('ExtractColour extract(), extracted:{}'.format(extracted))
        rgb = "({}, {}, {})".format(extracted['r'], extracted['g'], extracted['b'])
        hexstr = extracted['html_code']
        percentage = "Percentage: {}%".format(extracted['percentage'])
        res = "EXTRACT {}\n{}\n{}\n{}".format(self.state, rgb, hexstr, percentage)
        return res

    def get_photo_url(self):
        app.logger.debug('getphotourl, linkphotoid: {}'.format(
                         self.TELEGRAM_GET_FILE_API.format(
                             config.TELEGRAM_BOT_TOKEN, self.photo_id)))
        r = requests.get(self.TELEGRAM_GET_FILE_API.format(config.TELEGRAM_BOT_TOKEN,
                                                           self.photo_id))
        r.raise_for_status()
        j = r.json()
        app.logger.debug("getphotourl, json: {}".format(j))
        app.logger.debug('getphotourl, photourl: {}'.format(
                         self.TELEGRAM_FILE_URL.format(
                             config.TELEGRAM_BOT_TOKEN, j['result']['file_path'])))
        return self.TELEGRAM_FILE_URL.format(config.TELEGRAM_BOT_TOKEN,
                                             j['result']['file_path'])

    def __extract_method(self):
        self.state = ExtractColour.BGCOLOUR
        return self.__extract_method()

    def __extract_fgcolour(self):
        app.logger.debug('ExtractColour, __extract_fgcolour')
        return self.json['results'][0]['info']['foreground_colors'][0]

    def __extract_bgcolour(self):
        app.logger.debug('ExtractColour, __extract_bgcolour')
        return self.json['results'][0]['info']['background_colors'][0]
