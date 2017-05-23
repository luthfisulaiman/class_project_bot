from twitter import Twitter, OAuth


class Twitter_Search:

    def get_tweets(self, user):
        ACCESS_TOKEN = '222744252-Rlmt3vskun9X7mgwWx9ll8ur3CeAxFoXOGB2A7SC'
        ACCESS_SECRET = 'vmD6hqPKCkHpG8AxYNIqd5LhoJyooIGGyLokHYZnYcjwm'
        CONSUMER_KEY = 'srFihJdWAQ87008Y1fVUBZbx8'
        CONSUMER_SECRET = 'G2oiQTjd6Zgo2slmog2W5qYuDBHgc3iG00XNQFzabveN3KhJSD'

        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        twitter = Twitter(auth=oauth)
        tweetuser = twitter.statuses.user_timeline(screen_name=user, count=5)
        tln = ''
        for status in tweetuser:
            tln = tln + "%s\n" % (status["text"])
        return tln
