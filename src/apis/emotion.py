import json
from db import DBHelper

'''
Author: Ankit Kumar
Emotion Helper Class
Defines Functions to Return List of Keywords based on Emotion
'''

class EmotionHelper:
    '''
    Emotion Helper Class
    '''

    def __init__(self, args):
        self.logger = args['logger']
        self.logger.debug("Initialize Emotion Helper!")

        self.emotions = json.load(open(args['emotion_path']))
        self.ratings = json.load(open(args['rating_path']))
        self.dbHelper = DBHelper(dict(logger=self.logger))


    def get_emotion(self, rating):
        if rating >= self.ratings['excellent']:
            return self.emotions['excellent']
        elif rating >= self.ratings['good']:
            return self.emotions['good']
        elif rating >= self.ratings['neutral']:
            return self.emotions['neutral']
        elif rating >= self.ratings['bad']:
            return self.emotions['bad']
        else:
            return self.emotions['worst']
