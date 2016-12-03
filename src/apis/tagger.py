import nltk
import json
import os
from collections import Counter

'''
Author: Ankit Kumar
POS Tagger
Tags a tweet using parts of speech tags
'''

class Tagger:
    def __init__(self, args):
        self.logger = args['logger']
        self.config = json.load(open(args['tags_path']))

    def tagtweet(self, text):
        tokens = nltk.word_tokenize(text)
        tagged_text = nltk.pos_tag(tokens)

        return self.filtertweet(tagged_text)

    def filtertweet(self, tagged_text):
        words, tags = zip(*tagged_text)
        tag_counts = Counter(tags)
        nn_tag = 'NN'
        jj_tag = 'JJ'
        tag_len = len(tags)

        if nn_tag not in tag_counts or tag_counts[nn_tag] != self.config['nn_count']:
            return None
        elif jj_tag not in tag_counts or tag_counts[jj_tag] != self.config['jj_count']:
            return None

        if tag_len < self.config['min_tags'] or tag_len > self.config['max_tags']:
            return None

        return tags