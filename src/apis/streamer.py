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
        self.config = json.load(open(args['stream_path']))
        self.tagger = Tagger(dict(tags_path=args['tags_path'], logger=args['logger']))
        self.dbhelper = DBHelper(dict(logger=args['logger']))


    def on_status(self, status):
        # Process tweet and add to DB
        # Filter on Author Count
        author = status.author
        if author is not None:
            followers_count = author.followers_count
            if followers_count < self.config['followers_count']:
                return
        else:
            return

        # Filter on Tags
        tags = self.tagger.tagtweet(status.text)
        if tags is not None:
            # Add Tweet to DB
            tweet_id = status.id
            author_id = status.author.id
            tweet = dict(tweetid=tweet_id, authorid=author_id, tags=tags)
            print(tweet)
            #self.dbhelper.add_tweet(tweet)


    def on_error(self, status_code):
        # On Error
        assert False, "Error: %d" % (status_code,)

    def on_timeout(self):
        # On Timeout
        assert False, "Timeout..."