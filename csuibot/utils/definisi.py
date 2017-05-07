import requests


class Definisi:

    def __init__(self):
        self.url = "http://kateglo.com/api.php?format={}&phrase={}"

    def define(self, word):
        word = word.replace(' ', '%20')
        r = requests.get(self.url.format('json', word))

        if r.headers['Content-Type'] == 'application/json':
            jsonWord = r.json()
            wordType = jsonWord['kateglo']['lex_class_name']

            mean = {wordType: []}
            for definition in jsonWord['kateglo']['definition']:
                classWord = definition['lex_class_ref']

                if classWord is not None:
                    classWord = classWord.capitalize()
                    if classWord not in mean.keys():
                        mean[classWord.] = []
                    mean[classWord].append(definition['def_text'])
                else:
                    mean[wordType].append(definition['def_text'])

            output = ''

            for classWord in mean.keys():
                output += classWord + ':\n'
                i = 1
                for meaning in mean[classWord]:
                    output += str(i) + meaning + '\n'
                    i += 1
                output += '\n'
            return output
        else:
            return word + ' is not a word :(, maybe try another one?'
