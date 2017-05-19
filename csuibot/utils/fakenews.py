class FakeNews:
    JSON_URL = ("https://raw.githubusercontent.com/BigMcLargeHuge"
                "/opensources/master/sources/sources.json")
    JSON_FILE_LOC = (".sources_cache.json")
    json = None

    def __init__(self):
        pass

    def __save_json(self):
        pass

    def __load_json(self):
        pass

    def check(self, hostname):
        pass

    def add_filter(self, hostname, news_type):
        pass
