from db import TweetDB
import tweepy

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

    def on_status(self, status):
        # On Data Logic!
        print(status.text)

    def on_error(self, status_code):
        # On Error
        assert False, "Error: %d" % (status_code,)

    def on_timeout(self):
        # On Timeout
        assert False, "Timeout..."