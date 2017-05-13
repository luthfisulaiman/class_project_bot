import billboard


class NewAge_artist:
    """
    input: any part of artist's name
    output: all songs that contains artist's name
    """
    def __init__(self):
        self.chart = billboard.ChartData('new-age-albums')

    def find_newage_artist(self, name):
        resultsongs = ""
        err_msg = ("Artist is not present on chart or no such artist exists\n"
                   "Artist's name is case sensitive")
        for song in self.chart:
            if (name in song.artist):
                resultsongs += (song.artist+"\n"+song.title+"\n"+str(song.rank)+"\n")

        if (resultsongs == ""):
            return err_msg
        else:
            return resultsongs
