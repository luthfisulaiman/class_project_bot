import httplib

class IsUpWeb :
    def __init__(self, url):
        self.url = url

    def isUp(self) :
        connection = httplib.HTTPConnection(self._url)
        connection.request("HEAD", "/")
        respon = connection.getResponse()
        if respon.status == '200' :
            return "UP"
        else :
            return "DOWN"
