import requests as r
from bs4 import BeautifulSoup as bs


class JapanArtist:
    def __init__(self):
        self.url = "http://www.billboard.com/rss/charts/japan-hot-100"

    def getArtist(self, artist):
        MUSIC_NOTE = 'U+1F3B6'
        MICROPHONE = 'U+1F3A4'
        SPARKLES = 'U+2728'

        charts = r.get(self.url).text
        soup = bs(charts, 'html.parser')
        for chart in soup.find_all('item'):
            if(artist in chart.artist.string):
                return "Artist {}: {}\nSong {}: {}\nPosition {}: {}"\
                        .format(MICROPHONE, chart.artist.string, MUSIC_NOTE,
                                chart.chart_item_title.string, SPARKLES,
                                chart.rank_this_week.string)
        else:
            return "Artist not present on the Top 100 Chart"
