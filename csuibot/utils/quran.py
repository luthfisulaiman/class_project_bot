import json
import random


class quran:
    def __init__(self):
        with open('csuibot/utils/quran.json', 'r', encoding='utf-8') as quran_json:
            self.quran = json.load(quran_json)
        # print(self.quran)
        with open('csuibot/utils/quran-translation.json', 'r', encoding='utf-8') as qurantr_json:
            self.qurantr = json.load(qurantr_json)

    def lookup_quran(self, chapter, verse):
        try:
            chapter = int(chapter)
            verse = int(verse)
            ayat = self.quran['data']['surahs'][chapter]['ayahs'][verse]['text']
            translation = self.qurantr['data']['surahs'][chapter]['ayahs'][verse]['text']
            return ayat[::-1] + "\n" + translation + "\n"
        except IndexError:
            return "Please enter the valid chapter and verse"

    def get_surah(self, chapter):
        chapter = int(chapter)
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
