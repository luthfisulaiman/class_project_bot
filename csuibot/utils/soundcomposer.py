import soundcloud

class SoundComposer:
	def __init__(self, username):
		self.client_id = MY_CLIENT_ID
		self.client = soundcloud.Client(self.client_id)
		self.id_url = 'http://soundcloud.com/' + username

	def get_composer(self):
		track_treshold = 5
		# checking token
		if (self.client_id == 'MY_CLIENT_ID'):
			# resolve user url to user resource
			user = client.get('/resolve',url = self.id_url)
			track_fetched = 0
			track_message = ""
			for track in client.get('/users/%d/tracks' % user.id):
				track_message += track.title + '/n' + \
				                 track.duration + '/n' + \
				                 track.permalink_url + '/n /n'
				track_fetched += 1
				if(track_fetched == 5) break

			return track_message
       else :
       		return 	  'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'LIONE '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'LIONE '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'LIONE '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'LIONE '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
                      'The Chainsmokers - Closer (LIONE Remix) '\
                      '4:45 '\
                      'LIONE '\
                      'https://soundcloud.com/iamlione/the-chainsmokers-closer-lione-remix '\
