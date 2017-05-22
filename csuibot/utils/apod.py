import datetime
import os
from nasa import apod

os.environ["NASA_API_KEY"] = ('0hiSWsJgnhiT6xjtqO2txNrMpiAtswuIKgVSxUE6')


class Apod:

    @classmethod
    def fetch_apod(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        picture = apod.apod(today)
        return picture.url
