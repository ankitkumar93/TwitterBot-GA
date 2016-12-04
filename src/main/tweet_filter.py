import tweepy
import json
from apis.filter import Filter
from apis.db import DBHelper

'''
Author: Ankit Kumar
Tweet Filter Module
Get Tweets from DB and Filter Them
Push Tweets that satisfy the Constraint to Filter DB
'''

class TweetFilter:
    '''
    Tweet Fetcher Class
    '''

    def __init__(self, args):
        self.logger = args.logger
        self.logger.debug("Setting Up Stream!")

        config = json.load(open(args.config))

        self.filter = Filter(dict(logger=args.logger, filter_path=config['filter_path']))
        self.db = DBHelper(dict(logger=args.logger))

    def run(self):
        self.logger.debug("Starting to Filter Tweets!")

        # Initialize count for filtered tweets
        filtered_tweets_count = 0

        # Get All Tweets
        tweets = self.db.get_tweets(0)

        # Filter Tweets
        for tweet in tweets:
            if self.filter.check(tweet):
                filtered_tweet = dict(tweetid=filtered_tweet['tweetid'], tags=filtered_tweet['tags'], lrscore=0)
                self.db.add_filtered_tweet(filter_tweet)

                filtered_tweets_count += 1



def filter_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetFilter = TweetFilter(args)
    tweetFilter.run()