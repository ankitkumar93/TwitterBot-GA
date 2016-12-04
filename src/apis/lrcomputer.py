from apis.tweet import TweetHelper
import json

'''
Author: Ankit Kumar
LR Score Computer: Computes the LR Score for Tweets
'''

class LRComputer:
    def __init__(self, args):
        self.logger = args['logger']
        self.tweethelper = TweetHelper(dict(logger=args['logger'], keyPath=args['keyPath']))

    def compute(tweetid):
        # Compute LR Score
        retweets_val = self.tweethelper.get_num_retweets(tweetid)
        favorites_val = self.get_num_favorites(tweetid)

        return (retweets_val + favorites_val)