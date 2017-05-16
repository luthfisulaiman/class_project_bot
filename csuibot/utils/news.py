import requests
import json


class News:

    def get_news(query):
        url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'
        payload = {'q': query}
        headers = {'Ocp-Apim-Subscription-Key': '11491c9b135d4b4395430dd7c109fce3'}
        r = requests.get(url, params=payload, headers=headers)
        news = r.json()
        out = ''
        for values in news['value'][0:5]:
            out += ("[" + values['name'] + "]\n\n")
            out += (values['description'] + "\n")
            out += ("LINK: " + values['url'] + "\n\n\n")
        res = {'type': news['_type'], 'value': out}
        return res
