import requests


class News:

    def get_news(self, query):
        url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'
        payload = {'q': query}
        headers = {'Ocp-Apim-Subscription-Key': '11491c9b135d4b4395430dd7c109fce3'}
        r = requests.get(url, params=payload, headers=headers)
        news = r.json()
        return news
