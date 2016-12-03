import ntlk
import json
from collections import Counter

'''
Author: Ankit Kumar
POS Tagger
Tags a tweet using parts of speech tags
'''

class Tagger:
    def __init__(args):
        self.tokenize = ntlk.tokenize
        self.tag = nltk.tag
        self.taglist = json.load(open(args['tags_path']))

    def tag(text):
        tokens = self.tokenize(text)
        tags = self.tag(tokens)

        return self.filter(tags)

    def filter(tags):
        counts = Counter(tags)

        if len(counts) == len(taglist)
            return None

        for tag in taglist:
            if tag not in counts:
                return None
            elif !(tag.min <= counts[tag] && counts[tag] <= tag.max):
                return None

        return tags