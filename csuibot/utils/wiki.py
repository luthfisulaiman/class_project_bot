import wikipedia


class Wiki:

    def __init__(self, term):
        self.term = term

    def get_result(self):
        summary = wikipedia.summary(self.term)
        wikis = wikipedia.search(self.term)
        wiki = wikipedia.page(wikis[0])
        return summary + '\n\nsource: ' + wiki.url
