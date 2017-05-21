import requests
from random import randint
from urllib.parse import quote
import urllib


class ItunesPreviewer():

    def __init__(self):
        self.songs = []

    def get_preview(self, artist):
        search_result = ItunesRequester.make_request(artist)
        self.add_artist_song(search_result, artist)

        if not self.songs:
            raise ValueError("Can\'t found the requested artist")
        surprise_me = randint(0, len(self.songs) - 1)
        return self.songs[surprise_me]['previewUrl']

    def add_artist_song(self, lists, artist):
        for item in lists:
            if(item['artistName'].lower() == artist.lower()):
                self.songs.append(item)


class ItunesRequester():

    @staticmethod
    def make_request(artist):
        url = "https://itunes.apple.com/search?"
        en_artist = "term=" + quote(str(artist), safe='')
        media = "media=music"
        url = url + "{}&{}".format(en_artist, media)
        res = requests.get(url)
        return res.json()['results']


class ItunesLogo:

    def __init__(self):
        self.logo = ('https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Download_'
                     'on_iTunes.svg/2000px-Download_on_iTunes.svg.png')

    def get_logo(self):
        return self.logo


class MusicDownloader:

    def __init__(self):
        self.url = ""

    def set_url(self, url):
        self.url = url

    def download(self):
        urllib.request.urlretrieve(self.url, "preview.mp3")


def req_preview(artist):
    previewer = ItunesPreviewer()
    downloader = MusicDownloader()
    logo = ItunesLogo()
    url = previewer.get_preview(artist)
    downloader.set_url(url)
    downloader.download()

    return {"result": url, "logo": logo.get_logo()}
