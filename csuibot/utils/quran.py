import json
import random


class quran:
    def __init__(self):
        file = open('csuibot/utils/quran.json')
        self.quran = json.load(file)
        file = open('csuibot/utils/quran-translation.json')
        self.qurantr = json.load(file)

    def lookup_quran(self, chapter, verse):
        try:
            ayat = self.quran['data']['surahs'][chapter]['ayahs'][verse]['text']
            translation = self.qurantr['data']['surahs'][chapter]['ayahs'][verse]['text']
            return ayat[::-1] + "\n" + translation + "\n"
        except IndexError:
            return "Please enter the valid chapter and verse"

    def get_surah(self, chapter):
        ayat = self.quran['data']['surahs'][chapter]['englishName']
        return ayat

    def get_random_ayah(self):
        try:
            chapter = random.random() * 114
            verse = random.random() * len(self.quran['data']['surahs'][chapter]['ayahs'])
            ayat = self.quran['data']['surahs'][chapter]['ayahs'][verse]['text']
            translation = self.qurantr['data']['surahs'][chapter]['ayahs'][verse]['text']
            return ayat[::-1] + "\n" + translation + "\n"
        except IndexError:
            return "Please enter the valid chapter and verse"
