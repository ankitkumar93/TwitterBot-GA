import tweepy
import json
from apis.lrscore import LRScore
from apis.db import DBHelper

'''
Author: Ankit Kumar
Tweet LRScore Module
Computer LRScore for Tweets
'''

class TweetLRScore:
    '''
    Tweet LR Computer Class
    '''

    def __init__(self, args):
        self.logger = args.logger

        config = json.load(open(args.config))

        self.lrcomputer = LRScore(dict(logger=args.logger, key_path=config['key_path'], lrscore_path=config['lrscore_path']))
        self.db = DBHelper(dict(logger=args.logger))

    def run(self):
        self.logger.debug("Starting to Computer LRScore for Tweets!")

        # Get All Tweets
        tweets = self.db.get_filtered_tweets(0)

        # Computer LRScore for Tweets
        for tweet in tweets:
            tweetid = tweet['tweetid']
            lrscore self.lrcomputer.compute(tweetid)
                self.db.update_filtered_tweet(tweetid, lrscore)



def lrscore_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetLRScore = TweetLRScore(args)
    tweetLRScore.run()