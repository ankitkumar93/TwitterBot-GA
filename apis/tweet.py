import json
import tweepy
'''
Author: Anand Purohit
Twitter API Helper class to allow a few basic functions
'''

class TweetHelper:
    '''
    Tweet Helper class (Wrapper methods to do stuff with Tweepy)
    '''

    def __init__(self, logger):
        self.logger = logger
        key = json.load(open('key.json'))
        self.auth = tweepy.OAuthHandler(key['consumer_key'], key['consumer_secret'])
        self.auth.set_access_token(key['access_token'], key['access_secret'])
        self.api = tweepy.API(self.auth)

    def post_tweet(self, msg):
        self.logger.debug("Posting status: %s" % msg)
        self.api.update_status(msg)
        self.logger.debug("\"%s\" posted succesfully" % msg)

    def get_status(self, id):
        self.logger.debug("Fetching status for tweet-id: %s" % id)
        status = self.api.get_status(id)
        self.logger.debug("Status fetched successfully for tweet-id: %s" % id)
        return status

    def get_num_favorites(self, id):
        self.logger.debug("Fetching favorites for tweet-id: %s" % id)
        status = self.get_status(id)
        return status.favorite_count

    def get_num_retweets(self, id):
        self.logger.debug("Fetching retweets for tweet-id: %s" % id)
        status = self.get_status(id)
        return status.retweet_count

# helper = TweetHelper(None)
# print(helper.get_num_favorites("792639337741647872"))
# print(helper.get_num_retweets("792639337741647872"))