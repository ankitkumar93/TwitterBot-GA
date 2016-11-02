import nltk
import json
import tracery

from tracery.modifiers import base_english
from nltk.corpus import wordnet as wn

'''
Author: Anand Purohit
PyTracery helper class to allow a few basic functions
'''

class TraceryHelper:
    '''
    Helper class to deal with PyTracery (wrapper methods to help use PyTracery)
    '''
    def __init__(self, args):
        self.logger = args['logger']
        self.grammar_json = json.load(open(args['grammarPath']))

    def load_grammar(self):
        return tracery.Grammar(self.grammar_json)

    # def gen_emotional_word(self, emotion):
    #     return emotion

    def gen_sentence(self, args):
        game_name = args['game_name']
        emotion = args['emotion']
        syntax = args['syntax']

        # emotional_word = self.gen_emotional_word(emotion)
        self.grammar_json['emotional_word'] = emotion
        self.grammar_json['game_name'] = game_name
        self.grammar_json['syntax'] = syntax

        grammar = self.load_grammar()
        grammar.add_modifiers(base_english)
        return grammar.flatten("#syntax#")
