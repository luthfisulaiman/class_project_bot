import requests


class Definisi:

    def __init__(self):
        self.url = "http://kateglo.com/api.php?format={}&phrase={}"

    def define(self, word):
        word = word.replace(' ', '%20')
        r = requests.get(self.url.format('json', word))

        if r.headers['Content-Type'] == 'application/json':
            jsonword = r.json()
            wordtype = jsonword['kateglo']['lex_class_name']

            mean = {wordtype: []}
            for definition in jsonword['kateglo']['definition']:
                classword = definition['lex_class_ref']

                if classword is not None:
                    classword = classword.capitalize()
                    if classword not in mean.keys():
                        mean[classword] = []
                    mean[classword].append(definition['def_text'])
                else:
                    mean[wordtype].append(definition['def_text'])

            output = ''

            for classword in mean.keys():
                output += classword + ':\n'
                i = 1
                for meaning in mean[classword]:
                    output += str(i) + '. ' + meaning + '\n'
                    i += 1
                output += '\n'
            return output
        else:
            return word + ' is not a word :(, maybe try another one?'
