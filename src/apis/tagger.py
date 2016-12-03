import nltk

'''
Author: Ankit Kumar
POS Tagger
Tags a tweet using parts of speech tags
'''

class Tagger:
    def __init__(self, args):
        self.logger = args['logger']

    def tagtweet(self, text):
        tokens = nltk.word_tokenize(text)
        tagged_text = nltk.pos_tag(tokens)
        words, tags = zip(*tagged_text)

        return tags