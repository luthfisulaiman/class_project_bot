import requests as r


class Kelaskata:
    def __init__(self, message):
        self.webservice = "http://kateglo.com/api.php?format=json&phrase="
        self.message = message

    def getkelaskata(self):
        res = r.get(self.webservice + self.message)
        return (self.message + "/"+res.json()['kateglo']['lex_class'])
