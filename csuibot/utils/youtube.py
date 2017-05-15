from bs4 import BeautifulSoup as bs
import requests as r
from requests.exceptions import MissingSchema


class Youtube:

    def __init__(self):
        self.headers = {"Accept-Language": "en-US,en;q=0.5"}

    def getURL(self, url):
        if "youtube.com/watch?" not in url:
            return "Please provide a YouTube video URL"

        try:
            video = r.get(url, headers=self.headers)
        except MissingSchema:
            return "Invalid URL, do you mean http://{} ?".format(url)

        try:
            soup = bs(video.text, 'html.parser')
            header = soup.find(id="watch-header")
            information_div = header.find(id="watch8-action-buttons")\
                                    .find(id="watch8-sentiment-actions")

            title = soup.find(id="eow-title").string.strip()
            channel = header.find(id="watch7-user-header").div.a.string
            views = information_div.div.find(class_="watch-view-count").string
            likes = information_div.span.contents[1].button.span.string
            dislikes = information_div.span.contents[5].button.span.string
        except AttributeError:
            return "Video doesn't exist"
        else:
            return "{}\n{}\n{}\n{} likes & {} dislikes".format(title,
                                                               channel,
                                                               views,
                                                               likes,
                                                               dislikes)
