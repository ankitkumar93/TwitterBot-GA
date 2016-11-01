from db import DBHelper

'''
Author: Ankit Kumar
Emotion Helper Class
'''

class EmotionHelper
    '''
    Emotion Helper Class
    '''

    def __init__(self, args):
        self.logger = args.logger
        self.logger.debug("Initialize Emotion Helper!")

        self.emotions = json.load(open(args.emotionPath))
        self.ratings = json.load(open(args.ratingPath))
        self.dbHelper = DBHelper(dict(logger=self.logger))


    def get_emotion(self, rating):
        if rating >= ratings.excellent:
            return emotions.excellent
        elif rating >= ratings.good:
            return emotions.good
        elif rating >= ratings.neutral:
            return emotions.neutral
        elif rating >= ratings.bad:
            return emotions.bad
        else:
            return emotions.worse


