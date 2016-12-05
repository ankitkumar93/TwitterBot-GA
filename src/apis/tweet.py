import json
import tweepy
import time
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
        key = json.load(open(args['key_path']))
        self.auth = tweepy.OAuthHandler(key['consumer_key'], key['consumer_secret'])
        self.auth.set_access_token(key['access_token'], key['access_secret'])
        self.api = tweepy.API(self.auth)

        # Rate Initialization
        self.status_rate = 0

        # Sleep Time (in seconds)
        self.status_reset_time = 900

    def post_tweet(self, msg):
        self.logger.debug("Posting status: %s" % msg)
        self.api.update_status(msg)
        self.logger.debug("\"%s\" posted succesfully" % msg)

    def get_status(self, id):
        if self.status_rate == 800:
            self.logger.warning("Rate Limit Reached. Going to sleep!")
            time.sleep(self.status_reset_time)
            self.status_rate = 0

        try:
            self.logger.debug("Fetching status for tweet-id: %s" % id)
            status = self.api.get_status(id)
            self.logger.debug("Status fetched successfully for tweet-id: %s" % id)
            self.status_rate += 1
            return status
        except tweepy.error.RateLimitError:
            assert False, "Rate limit exceeded!"
        except tweepy.error.TweepError:
            self.logger.warning("Tweet Status not found for id: %d" % id)
        
    def get_num_lr(self, id):
        self.logger.debug("Fetching favorites for tweet-id: %s" % id)
        status = self.get_status(id)
        if status is None:
            return 0, 0
        
        return status.favorite_count, status.retweet_count
        
    def get_num_favorites(self, id):
        self.logger.debug("Fetching favorites for tweet-id: %s" % id)
        status = self.get_status(id)
        if status is None:
            return 0

        return status.favorite_count
        
    def get_num_retweets(self, id):
        self.logger.debug("Fetching retweets for tweet-id: %s" % id)
        status = self.get_status(id)
        if status is None:
            return 0

        return status.retweet_count

    def get_user_from_status(self, status):
        self.logger.debug("Getting user from status with tweet-id: %s" % status.id_str)
        return status.user

    def get_user_from_tweet_id(self, id):
        self.logger.debug("Fetching user from tweet-id: %s" % id)
        status = self.get_status(id)
        return status.user

    def get_followers_count(self, user):
        self.logger.debug("Getting followers count from user with screen name: %s" % user.screen_name)
        return user.followers_count

    def get_followers_count_from_user_id(self, id):
        self.logger.debug("Fetching followers count for user with id: %s" % id)
        user = self.api.get_user(id)
        self.logger.debug("User fetched successfully for user-id: %s" % id)
        return user

    def get_users_who_mentioned_keyword(self, search_keyword):
        self.logger.debug("Fetching tweets for the keyword: %s" % search_keyword)
        users = set()
        for tweet in tweepy.Cursor(self.api.search, q=search_keyword, count=100).items(100):
            users.add(tweet.user)
        self.logger.debug("Results fetched successfully for keyword: %s" % search_keyword)
        return users
