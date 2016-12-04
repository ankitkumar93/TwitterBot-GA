from apis.tweet import TweetHelper
import json

'''
Author: Ankit Kumar
LR Score Computer: Computes the LR Score for Tweets
'''

class LRComputer:
    def __init__(self, args):
        self.logger = args['logger']
        self.tweethelper = TweetHelper(dict(logger=args['logger'], key_path=args['key_path']))

    def compute(self, tweetid):
        # Compute LR Score
        try:
            retweets_val = self.tweethelper.get_num_retweets(tweetid)
            favorites_val = self.tweethelper.get_num_favorites(tweetid)
        except tweepy.error.TweepError:
            self.logger.warning("Tweet Status not found for tweetid: %d" % tweetid)

        return (retweets_val + favorites_val)