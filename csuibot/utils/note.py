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
        notes = None
        try:
            f = open('notes.json', 'r')
            notes = json.load(f)
            f.close()
        except (FileNotFoundError, json.JSONDecodeError):
            notes = []

        notes.append(self.text)
        with open('notes.json', 'w') as f:
            json.dump(notes, f)

        return 'Notes added'
