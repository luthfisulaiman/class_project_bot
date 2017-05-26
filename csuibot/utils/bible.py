import json
import random


class Bible:
    def __init__(self):
        bible_file = open("csuibot/utils/data/matthew.json", "r")
        matthew = json.load(bible_file)
        bible_file = open("csuibot/utils/data/mark.json", "r")
        mark = json.load(bible_file)
        bible_file = open("csuibot/utils/data/luke.json", "r")
        luke = json.load(bible_file)
        bible_file = open("csuibot/utils/data/john.json", "r")
        john = json.load(bible_file)
        bible_file.close()
        self.json_bible = {"matthew": matthew["book"],
                           "mark": mark["book"],
                           "luke": luke["book"],
                           "john": john["book"]}

    def get_verse(self, book, chapter_num, verse_num):
        return self.json_bible[book][str(chapter_num)]["chapter"][str(verse_num)]["verse"]

    def random_verse(self):
        random_book = random.choice(list(self.json_bible.keys()))
        random_chapter = random.randint(1, len(self.json_bible[random_book]))
        random_verse = random.randint(1, len(self.json_bible[random_book]
                                             [str(random_chapter)]["chapter"]))
        verse = self.json_bible[random_book][str(random_chapter)][
            "chapter"][str(random_verse)]["verse"]
        return (random_book, verse)

    def get_total_chapter(self, book):
        return len(self.json_bible[book])

    def get_total_verse(self, book, chapter_num):
        return len(self.json_bible[book][str(chapter_num)]["chapter"])
