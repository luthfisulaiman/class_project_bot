import requests


class Crop:
    def do_crop(self, file):
        api_key = 'acc_bcb31745da643f1'
        api_secret = '9e35b9c1a2ffbdcc16e35998fa962238'

        response = requests.get('https://api.imagga.com/v1/croppings?url=' + file +
                                '&resolution=100x100', auth=(api_key, api_secret))

        x1 = response.json()['results'][0]['croppings'][0]['x1']
        y1 = response.json()['results'][0]['croppings'][0]['y1']
        x2 = response.json()['results'][0]['croppings'][0]['x2']
        y2 = response.json()['results'][0]['croppings'][0]['y2']
        message_1 = '<x1, y1> : <{}, {}>\n'.format(x1, y1)
        message_2 = '<x2, y2> : <{}, {}>\n'.format(x2, y2)
        message = message_1 + message_2
        return message