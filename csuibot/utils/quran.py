import json

class quran:
    def __init__(self):
    	file = open('csuibot/utils/quran.json', 'r')
    	self.quran = json.load(file)
    	file = open('csuibot/utils/quran-translation.json', 'r')
    	self.quran-translation = json.load(file)

    def lookup_Quran(self, chapter, verse):
    	pass

