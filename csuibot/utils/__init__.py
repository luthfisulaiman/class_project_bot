from csuibot.utils import zodiac as z
import urllib.request
import json


def lookup_zodiac(month, day):
    zodiacs = [
        z.Aries(),
        z.Taurus(),
        z.Gemini(),
        z.Cancer(),
        z.Leo(),
        z.Virgo(),
        z.Libra(),
        z.Scorpio(),
        z.Sagittarius(),
        z.Capricorn(),
        z.Aquarius(),
        z.Pisces()
    ]

    for zodiac in zodiacs:
        if zodiac.date_includes(month, day):
            return zodiac.name
    else:
        return 'Unknown zodiac'


def lookup_chinese_zodiac(year):
    num_zodiacs = 12
    zodiacs = {
        0: 'rat',
        1: 'buffalo',
        2: 'tiger',
        3: 'rabbit',
        4: 'dragon',
        5: 'snake',
        6: 'horse',
        7: 'goat',
        8: 'monkey'
    }
    ix = (year - 4) % num_zodiacs

    try:
        return zodiacs[ix]
    except KeyError:
        return 'Unknown zodiac'


def lookup_sentiment_new(text):
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    sentiment_api = 'text/analytics/v2.0/sentiment'
    sentimentUri = base_url + sentiment_api
    apiKey = '4c831ddf14ba43bd98d6f1aa527b3de6'
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = apiKey
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    postData1 = json.dumps({"documents": [{"id": "1", "language": "en", "text": text}]})
    postData2 = postData1.encode('utf-8')
    request2 = urllib.request.Request(sentimentUri, postData2, headers)
    response2 = urllib.request.urlopen(request2)
    response2json = json.loads(response2.read().decode('utf-8'))
    sentiment = response2json['documents'][0]['score']
    return ('Sentiment:  %f' % sentiment)
