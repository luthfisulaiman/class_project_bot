import requests
from random import randint
from urllib.parse import quote
import urllib
import os


class ItunesPreviewer():

    def __init__(self):
        self.songs = []

    def get_preview(self):
        if not self.songs:
            raise ValueError("Can\'t found the requested artist")
        surprise_me = randint(0, len(self.songs) - 1)
        return self.songs[surprise_me]['previewUrl']

    def add_artist_song(self, lists, artist):
        for item in lists:
            if(item['artistName'].lower() == artist.lower()):
                self.songs.append(item)


class ItunesRequester():

    def __init__(self):
        self.url = "https://itunes.apple.com/search?"

    def request(self, artist):
        en_artist = "term=" + quote(str(artist), safe='')
        media = "media=music"
        task = self.url + "{}&{}".format(en_artist, media)
        res = requests.get(task)
        return res.json()['results']


class MusicDownloader:

    def __init__(self):
        self.url = ""

    def set_url(self, url):
        self.url = url

    def download(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "preview.mp3"))
        urllib.request.urlretrieve(self.url, path)


class Manager:

    def __init__(self):
        self._downloader = MusicDownloader()
        self._previewer = ItunesPreviewer()
        self._requester = ItunesRequester()

    def get_preview(self, artist):
        req = self._requester.request(artist)
        self._previewer.add_artist_song(req, artist)
        self.url = self._previewer.get_preview()

    def download_url(self):
        self._downloader.set_url(self.url)
        self._downloader.download()
