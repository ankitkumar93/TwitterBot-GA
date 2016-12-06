from db import DBHelper
import tweepy
import json
from tagger import Tagger

'''
Author: Ankit Kumar
Streamer API to Stream Data from Twitter
Uses the DB API
Uses the Twitter API
Defines Interface to Stream Data
'''

class StreamListener(tweepy.StreamListener):
    '''
    Stream Listener
    Overriden to Add Logic to on_status
    '''

    def setup(self, args):
        self.tagger = Tagger(dict(logger=args['logger']))
        self.dbhelper = DBHelper(dict(logger=args['logger']))


    def on_status(self, status):
        # Process tweet and add to DB
        tweet_id = status.id
        followers_count = status.author.followers_count
        author_id = status.author.id
        tags = self.tagger.tagtweet(status.text)
        
        tweet = dict(tweetid=tweet_id, authorid=author_id, tags=tags, followers=followers_count)
        self.dbhelper.add_tweet(tweet)


    def on_error(self, status_code):
        # On Error
        assert False, "Error: %d" % (status_code,)

    def on_timeout(self):
        # On Timeout
        assert False, "Timeout..."