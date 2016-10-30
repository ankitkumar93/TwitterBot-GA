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

    def __init__(self, args):
        self.logger = args['logger']
        key = json.load(open(args['keyPath']))
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

    def get_user_from_status(self, status):
        self.logger.debug("Getting user from status with tweet-id: %s" % status.id_str)
        return status.user

    def get_user_from_tweet_id(self, id):
        self.logger.debug("Fetching user from tweet-id: %s" % id)
        status = self.get_status(id)
        return status.user

    def get_followers_count(self, user):
        # self.logger.debug("Getting followers count from user with screen name: %s" % user.screen_name)
        return user.followers_count

    def get_followers_count_from_user_id(self, id):
        self.logger.debug("Fetching followers count for user with id: %s" % id)
        user = self.api.get_user(id)
        self.logger.debug("User fetched successfully for user-id: %s" % id)
        return user

    def get_users_who_mentioned_keyword(self, search_keyword):
        # self.logger.debug("Fetching tweets for the keyword: %s" % search_keyword)
        users = set()
        for tweet in tweepy.Cursor(self.api.search, q=search_keyword, count=100).items(100):
            users.add(tweet.user)
        # self.logger.debug("Results fetched successfully for keyword: %s" % search_keyword)
        return users


# helper = TweetHelper(None)
# print(helper.get_num_favorites("792639337741647872"))
# users = helper.get_users_who_mentioned_keyword("Titanfall 2")
# for user in users:
#     print ("Getting followers count for %s: %d" % (user, helper.get_followers_count(user)))
# print(helper.get_num_retweets("792639337741647872"))
