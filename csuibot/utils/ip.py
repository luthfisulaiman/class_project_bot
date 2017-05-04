from urllib.request import urlopen, URLError


class IP:

    @classmethod
    def ip(self):
        try:
            return urlopen("https://api.ipify.org").read().decode('utf-8')
        except URLError:
            return 'Error connecting to ipify, please try again later'
