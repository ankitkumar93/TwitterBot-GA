import tweepy
import json
from apis.lrcomputer import LRComputer
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
        self.lrcomputer = LRComputer(dict(logger=args.logger, key_path=config['key_path']))
        self.db = DBHelper(dict(logger=args.logger))

    def run(self):
        self.logger.debug("Starting to Compute LRScore for Tweets!")

        # Get All Tweets
        tweets = self.db.get_filtered_tweets()

        # Computer LRScore for Tweets
        maxLRScore = 0
        for tweet in tweets:
            tweetid = tweet['tweetid']
            lrscore = self.lrcomputer.compute(tweetid)
            tweet['lrscore'] = lrscore
            maxLRScore = max(lrscore, maxLRScore)

        scaleUpValue = maxLRScore/float(2)
        maxLRScore += scaleUpValue

        # Normalize LRScore for Tweets
        Update in DB
        for tweet in tweets:
            tweet['lrscore'] = (tweet['lrscore'] + scaleUpValue)/maxLRScore
            self.db.update_filtered_tweet(tweet['tweetid'], tweet['lrscore'])


def lrscore_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetLRScore = TweetLRScore(args)
    tweetLRScore.run()