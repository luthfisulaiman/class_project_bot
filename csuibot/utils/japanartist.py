import requests as r
from bs4 import BeautifulSoup as bs


class JapanArtist:
    def __init__(self):
        self.url = "http://www.billboard.com/rss/charts/japan-hot-100"

    def getArtist(self, artist):

        charts = r.get(self.url).text
        soup = bs(charts, 'html.parser')
        for chart in soup.find_all('item'):
            if(artist.lower() == chart.artist.string.lower()):
                return "🎤 Artist 🎤  :{}\n\🎶 Song 🎶    :{}\n\📈 Position 📈:{}\n"\
                        .format(chart.artist.string,
                                chart.chart_item_title.string,
                                chart.rank_this_week.string)
        else:
            return "Artist not present on the Top 100 Chart"
