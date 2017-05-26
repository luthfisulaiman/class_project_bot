import json
import random


class quran:
    class __quran:
        def __init__(self):
            linkq = 'csuibot/utils/quran.json'
            linkqtr = 'csuibot/utils/quran-translation.json'
            with open(linkq, 'r', encoding='utf-8') as quran_json:
                self.quran = json.load(quran_json)
            with open(linkqtr, 'r', encoding='utf-8') as qurantr_json:
                self.qurantr = json.load(qurantr_json)

        def lookup_quran(self, chapter, verse):
            try:
                chapter = int(chapter)
                verse = int(verse)
                surah = self.quran['data']['surahs']
                surahtr = self.qurantr['data']['surahs']
                ayat = surah[chapter-1]['ayahs'][verse-1]['text']
                translation = surahtr[chapter-1]['ayahs'][verse-1]['text']
                return ayat + "\n" + translation + "\n"
            except IndexError:
                return "Please enter the valid chapter and verse"

        def get_chapter(self):
            chapter = []
            for data in (self.quran['data']['surahs']):
                chapter.append(data['englishName'])
            return chapter

        def get_random_ayah(self):
            try:
                chapter = int(random.random() * 114)
                surah = self.quran['data']['surahs']
                surahtr = self.qurantr['data']['surahs']
                verse = int(random.random()) * len(surah[chapter]['ayahs'])
                ayat = surah[chapter-1]['ayahs'][verse-1]['text']
                translation = surahtr[chapter-1]['ayahs'][verse-1]['text']
                surahName = surahtr[chapter-1]['englishName']
                return surahName + "@" + ayat + "\n" + translation + "\n"
            except IndexError:
                return "Please enter the valid chapter and verse"


instance = None


def __new__(cls):
    if not quran.instance:
        quran.instance = quran.__quran()
    return quran.instance
