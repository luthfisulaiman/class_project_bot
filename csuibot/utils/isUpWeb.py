import http.client

class IsUpWeb :
    def __init__(self, url):
        self._url = url

    def isUp(self) :
        connection = http.client.HTTPConnection(self._url)
        connection.request("HEAD", "/")
        respon = connection.getresponse()
        if respon.status == '200' :
            return "UP"
        else :
            return "DOWN"
