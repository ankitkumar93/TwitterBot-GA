import json
from apis.db import TweetDB

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

    def __init__(self, logger):
        self.logger = logger
        self.logger.debug("Seting Up Selector!")
        self.db = TweetDB(logger)

        config = json.load(open('config.json'))
        self.tweet_count = config['tweet_count']

    def select(self):
        self.logger.debug("Starting Selection!")
        tweets = self.db.get_tweets(self.tweet_count)
        if tweets is None:
            self.logger.warning("Tweet Cursor is None!")
        else:
            self.logger.debug("%d Tweets Found!" % (len(tweets),))
        return tweets