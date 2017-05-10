import requests
import os
import pycountry
import validators


class DetectLang:

    def __init__(self, arg):
        self._url = 'https://api.dandelion.eu/datatxt/li/v1'
        self.arg = arg

    def make_request(self):
        return requests.get('{}?token={}&{}={}'.format(
                self._url, os.environ['DANDELION_TOKEN'], self.get_type(), self.arg
            )
        ).json()

    def get_type(self):
        type = 'url'
        if validators.url(self.arg) is not True:
            type = 'text'
        return type

    def get_result(self):
        data = self.make_request()
        result = ''

        if 'error' not in data:
            for lang in data['detectedLangs']:
                result += '{} ({}%)\n'.format(
                    (pycountry.languages.get(alpha_2=lang['lang'])).name,
                    round(lang['confidence'] * 100, 2)
                )
        else:
            raise LookupError(data['message'])

        return result
