from .. import app
import requests

api_key = 'acc_639b88467681d49'
api_secret = 'c1ca154340d33c0c6feef02eaa2561f8'
telephoto_url = 'https://api.telegram.org/file/bot%s/%s'
imagga_link = 'https://api.imagga.com/v1/categorizations/nsfw_beta?url=%s'


def is_sfw(data):

    photo_url = telephoto_url % (app.config['TELEGRAM_BOT_TOKEN'], data)
    response = requests.get(imagga_link % photo_url, auth=(api_key, api_secret))

    response_json = response.json()
    results = response_json['results']
    if results == []:
        raise ValueError()

    categories = results[0]['categories']
    safe_or_nsfw = categories[0]['name']

    return safe_or_nsfw == 'safe'
