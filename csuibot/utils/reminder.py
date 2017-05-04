import time

class Reminder :

    def __init__(self, time, text) :
        self._second = int(time) * 60
        self._text = text

    def remind_text(self) :
        time.sleep(self._second)
        return self._text
