import random
import json

from db import DBHelper

'''
Author: Anand Purohit
Module to convert the structures obtained from GA into syntaxes that can be used in Tracery
'''


class SyntaxGen:
    def __init__(self, args):
        self.logger = args['logger']
        # Load Config
        config = json.load(open(args['sg_path']))
        # The number of tags beyond which we will not try to extend a syntax
        self.idealLength = config['ideal_length']
        # The probability with which we will join 2 structures in case a
        # structure does not lead to a large enough syntax
        self.conjunctionProb = config['conjunction_probability']
        # The probability of selecting "a/an" as opposed to "the" when using a determinant
        self.articleProb = config['article_probability']
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

        if tag == "NNPS":
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

        if tag == "NNS":
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
        if tag == "DT":
            return self.get_determinant_syntax(self.articleProb)
        elif tag == "NNP" or tag == "NNPS":
            return self.get_proper_noun_syntax(tag, useAhead)
        elif tag == "NN" or tag == "NNS":
            return self.get_noun_syntax(tag, useAhead)
        elif tag == "VBD" or tag == "VBN":
            return useAhead, "#VB.ed#"
        elif tag == "VBG":
            return useAhead, "#VB#ing"
        elif tag == "VBZ" or tag == "VBP":
            return useAhead, "#VB.s#"
        elif tag == "JJR":
            return useAhead, "#JJ#er"
        elif tag == "JJS":
            return useAhead, "#JJ#est"
        elif tag == "RBS":
            return useAhead, "#RB#est"
        else:
            return useAhead, "#" + tag + "#"

    '''
    Convert a structure that was generated from the GA (a list of tags) into a
    syntax that Tracery may be able to understand
    '''
    def create_syntax(self, tags):
        syntaxList = []
        useAhead = None
        for tag in tags:
            if tag == "." or tag == ",":
                lastWord = syntaxList.pop()
                lastWord += tag
                syntaxList.append(lastWord)
            else:
                useAhead, placeholder = self.create_syntax_word(tag, useAhead)
                syntaxList.append(placeholder)

        if len(tags) < self.idealLength:
            if random.random() < self.conjunctionProb:
                # Create a syntax for some other random structure that the GA produced
                extensionSyntax = self.dbHelper.get_random_syntax()
                # Join the existing syntax with that generated from the randomly chosen structure
                if extensionSyntax is not None:
                    syntaxList.append(self.create_syntax_word("CC", None))
                    syntaxList.append(extensionSyntax)

        return " ".join(syntaxList)
