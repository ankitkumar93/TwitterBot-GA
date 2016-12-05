import random

from db import DBHelper

'''
Author: Anand Purohit
Module to convert the structures obtained from GA into syntaxes that can be used in Tracery
'''


class SyntaxGen:
    def __init__(self, args):
        self.logger = args['logger']
        # The number of tags beyond which we will not try to extend a syntax
        self.idealLength = args['idealLength']
        # The probability with which we will join 2 structures in case a
        # structure does not lead to a large enough syntax
        self.conjunctionProb = args['conjunctionProbability']
        # The probability of selecting "a/an" as opposed to "the" when using a determinant
        self.articleProb = args['articleProbability']
        self.dbHelper = DBHelper(dict(logger=self.logger))

    '''
    This method assigns a value for the "useAhead" parameter which then propagates
    within the syntax till a noun is encountered.
    The generation of the "useAhead" parameter is governed by the probability of
    whether to replace the determiner tag with "a/an" or with "the".
    '''
    @staticmethod
    def get_determinant_syntax(articleProb):
        if random.random() < articleProb:
            return "a", ""
        else:
            return None, "the"

    '''
    This method may return 1 of 4 possible outputs -
        #NNP.capitalize# (if tag was for a singular proper noun and no useAhead exists),
        #NNP.capitalize.s# (if tag was for a plural proper noun and no useAhead exists),
        #NNP.capitalize.a# (if tag was for a singular proper noun and a useAhead exists), or
        #NNP.capitalize.a.s# (if tag was for a plural proper noun and a useAhead also exists)

    In any case, a call to this method will consume the value of "useAhead".
    '''
    @staticmethod
    def get_proper_noun_syntax(tag, useAhead):
        temp = "NNP.capitalize"

        if useAhead is not None:
            # There had been "a/an" before this proper noun
            temp += "." + useAhead

        if tag is "NNPS":
            # Proper noun plural
            temp += ".s"

        placeholder = "#" + temp + "#"
        return None, placeholder

    '''
    This method may return 1 of 4 possible outputs -
        #NN# (if tag was for a singular noun and no useAhead exists), 
        #NN.s# (if tag was for a plural noun and no useAhead exists),
        #NN.a# (if tag was for a singular noun and a useAhead exists), or
        #NN.a.s# (if tag was for a plural noun and a useAhead also exists)

    In any case, a call to this method will consume the value of "useAhead".
    '''
    @staticmethod
    def get_noun_syntax(tag, useAhead):
        temp = "NN"

        if useAhead is not None:
            # There had been "a/an" before this proper noun
            temp += "." + useAhead

        if tag is "NNS":
            # Proper noun plural
            temp += ".s"

        placeholder = "#" + temp + "#"
        return None, placeholder

    '''
    Method to convert a tag into a placeholder for the syntax to be generated
    Here, "tag" is the POS-tag that needs to be converted.
    "useAhead" is a parameter that allows the propagation of determinants, mainly the use of "a" and "an",
    which will mark the next noun (common or proper). The "useAhead" parameter is simply propagated further,
    and not consumed or modified, for any tag that does not represent a noun or a determiner
    '''
    def create_syntax_word(self, tag, useAhead):
        if tag is "DT":
            return self.get_determinant_syntax(self.articleProb)
        elif tag is "NNP" or tag is "NNPS":
            return self.get_proper_noun_syntax(tag, useAhead)
        elif tag is "NN" or tag is "NNS":
            return self.get_noun_syntax(tag, useAhead)
        elif tag is "VBD" or tag is "VBN":
            return useAhead, "#VB.ed#"
        elif tag is "VBG":
            return useAhead, "#VB#ing"
        elif tag is "VBZ" or tag is "VBP":
            return useAhead, "#VB.s#"
        elif tag is "JJR":
            return useAhead, "#JJ#er"
        elif tag is "JJS":
            return useAhead, "#JJ#est"
        elif tag is "RBS":
            return useAhead, "#RB#est"
        else:
            return useAhead, "#" + tag + "#"

    '''
    Convert a structure that was generated from the GA (a list of tags) into a
    syntax that Tracery may be able to understand
    '''
    def create_syntax(self, tags):
        syntax = ""
        useAhead = None
        for tag in tags:
            useAhead, placeholder = self.create_syntax_word(tag, useAhead)
            syntax += placeholder

        if len(tags) < self.idealLength:
            if random.random() < self.conjunctionProb:
                # Create a syntax for some other random structure that the GA produced
                extensionSyntax = self.create_syntax(self.dbHelper.get_random_syntax())
                # Join the existing syntax with that generated from the randomly chosen structure
                syntax += self.create_syntax_word("CC", None) + extensionSyntax

        return syntax
