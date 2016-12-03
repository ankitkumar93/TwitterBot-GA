import json
from apis.db import DBHelper

'''
Author: Ankit Kumar
Selector for Tweets
Selects N Tweets of a Certain type and Emotion
'''


class Selector:
    '''
    Selector Class
    Defines Methods to Select Tweets from DB based on Type and Emotion
    '''

    def __init__(self, args):
        self.logger = args['logger']
        self.logger.debug("Seting Up Selector!")
        self.db = DBHelper(dict(logger=self.logger))

        self.game_count = args['game_count']

    def select(self):
        self.logger.debug("Starting Selection!")
        games = self.db.get_games(self.game_count)
        if games is None:
            self.logger.warning("Game Cursor is None!")
        else:
            self.logger.debug("%d Games Found!" % (len(games),))

        if self.game_count < len(games):
            self.game_count = len(games)
        return games[:self.game_count]