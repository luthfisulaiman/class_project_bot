import soundcloud

class SoundComposer:
    def __init__(self, username):
        self.username = username

    def get_composer(self):
        track_treshold = 5
        # checking token
        # resolve user url to user resource
        # using dummy because don't have the API

        # client = soundcloud.Client(self.client_id)
        # user = client.get('/resolve',url = self.id_url) 
        # tracks = client.get('/users/%d/tracks' % user.id)
        
        id_url = 'http://soundcloud.com/' + self.username
        user = {'id' : '2381'}
        tracks = [{'title' : 'The Chainsmokers - Closer (LIONE Remix)', 'duration' : '4:45 ', 'permalink_url' : 'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix'}, {'title' : 'The Chainsmokers - Closer (LIONE Remix)', 'duration' : '4:45 ', 'permalink_url' : 'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix'},{'title' : 'The Chainsmokers - Closer (LIONE Remix)', 'duration' : '4:45 ', 'permalink_url' : 'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix'},{'title' : 'The Chainsmokers - Closer (LIONE Remix)', 'duration' : '4:45 ', 'permalink_url' : 'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix'},{'title' : 'The Chainsmokers - Closer (LIONE Remix)', 'duration' : '4:45 ', 'permalink_url' : 'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix'}]
    
        track_message = ""
        for i in range(5):
            track_message += tracks[i]['title'] + '/n' + tracks[i]['duration'] + '/n' + self.username + '/n' + tracks[i]['permalink_url'] + '/n /n'
        
        return track_message