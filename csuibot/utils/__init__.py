from nltk.classify import NaiveBayesClassifier
from csuibot.utils import zodiac as z



def lookup_zodiac(month, day):
    zodiacs = [
        z.Aries(),
        z.Taurus(),
        z.Gemini(),
        z.Cancer(),
        z.Leo(),
        z.Virgo(),
        z.Libra(),
        z.Scorpio(),
        z.Sagittarius(),
        z.Capricorn(),
        z.Aquarius(),
        z.Pisces()
    ]

    for zodiac in zodiacs:
        if zodiac.date_includes(month, day):
            return zodiac.name
    else:
        return 'Unknown zodiac'


def lookup_chinese_zodiac(year):
    num_zodiacs = 12
    zodiacs = {
        0: 'rat',
        1: 'buffalo',
        2: 'tiger',
        3: 'rabbit',
        4: 'dragon',
        5: 'snake',
        6: 'horse',
        7: 'goat',
        8: 'monkey'
    }
    ix = (year - 4) % num_zodiacs

    try:
        return zodiacs[ix]
    except KeyError:
        return 'Unknown zodiac'


def word_feats(words):
    return dict([(word, True) for word in kata])


def lookup_sentiment(word):
    positive_vocab = ['good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love']
    negative_vocab = ['bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(']
    neutral_vocab = ['movie','the','sound','was','is','actors','did','know','words','not']
    positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
    negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
    neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
    train_set = negative_features + positive_features + neutral_features
    classifier = NaiveBayesClassifier.train(train_set)
    neg = 0
    pos = 0
    words = kata.split(' ')
    for i in words:
        classresult = classifier.classify(word_feats(i))
        if classresult == 'neg':
            neg = neg + 1
        if classresult == 'pos':
            pos = pos + 1
    try:
        return 'Positive: ' + str(float(pos)/len(words)) + '\nNegative: ' + str(float(neg)/len(words))
    except KeyError:
        return 'not found'    
