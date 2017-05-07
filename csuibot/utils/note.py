import json


class Notes:

    def __init__(self, text=''):
        self.text = text

    def view(self):
        with open('notes.json', 'r') as f:
            notes = json.load(f)
            view = 'List notes:\n'

            i = 1
            for note in notes:
                view += str(i) + '. ' + note + '\n'
                i += 1
        return view

    def write(self):
        with open('notes.json', 'a+') as f:
            notes = None
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                notes = []
            notes.append(self.text)
            json.dump(notes, f)
        return 'Notes added'
