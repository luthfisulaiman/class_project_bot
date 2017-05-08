# import soundcloud


class SoundComposer:
    def __init__(self, username):
        self.username = username
        self.client_id = APP_TOKEN

    def get_composer(self):
        # using dummy because don't have the SoundCloud client API

        # client = soundcloud.Client(self.client_id)
        # id_url = 'http://soundcloud.com/' + self.username

        # user = client.get('/resolve',url = self.id_url)

        # tracks = client.get('/users/%d/tracks' % user.id)
        tracks = [{'title': 'The Chainsmokers - Closer (LIONE Remix)', 'duration': '4:45 ',
                  'permalink_url': 'https://soundcloud.com/iamlione/\
                  the-chainsmokers-closer-lione-remix'},
                  {'title': 'The Chainsmokers - Closer (LIONE Remix)', 'duration': '4:45 ',
                  'permalink_url': 'https://soundcloud.com/iamlione/\
                  the-chainsmokers-closer-lione-remix'},
                  {'title': 'The Chainsmokers - Closer (LIONE Remix)', 'duration': '4:45 ',
                  'permalink_url': 'https://soundcloud.com/iamlione/\
                  the-chainsmokers-closer-lione-remix'},
                  {'title': 'The Chainsmokers - Closer (LIONE Remix)', 'duration': '4:45 ',
                  'permalink_url': 'https://soundcloud.com/iamlione/\
                  the-chainsmokers-closer-lione-remix'},
                  {'title': 'The Chainsmokers - Closer (LIONE Remix)', 'duration': '4:45 ',
                  'permalink_url': 'https://soundcloud.com/iamlione/\
                  the-chainsmokers-closer-lione-remix'}]

        track_message = ""
        for i in range(5):
            track_message += tracks[i]['title'] + '\n' + tracks[i]['duration'] + '\n' + \
                             self.username + '\n' + tracks[i]['permalink_url'] + '\n \n'

        return track_message
