import billboard


class Hot100_artist:
    """
    input: any part of artist's name
    output: all songs that contains artist's name
    """
    def __init__(self):
        self.chart = billboard.ChartData('hot-100')

    def find_hot100_artist(self, name):
        resultsongs = ""
        err_msg = ("Artist is not present on chart or no such artist exists\n"
                   "Artist's name is case sensitive")
        for song in self.chart:
            if (name in song.artist):
                resultsongs += (song.artist+"\n"+song.title+"\n"+str(song.rank))

        if (resultsongs == ""):
            return err_msg
        else:
            return resultsongs
