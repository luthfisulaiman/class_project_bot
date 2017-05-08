import requests as r


class Password:

    def __init__(self):
        self.url = 'http://www.sethcardoza.com/api/rest/tools/' \
                   'random_password_generator/length:{}'

    def generate_password(self, len):
        if 1 <= len <= 128:
            target = self.url.format(len)
            return r.get(target).text
        else:
            return 'Only a single integer, 1-128, is allowed as length'
