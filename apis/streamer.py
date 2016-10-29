from db import TweetDB
import tweetpy

'''
Author: Ankit Kumar
Streamer API to Stream Data from Twitter
Uses the DB API
Uses the Twitter API
Defines Interface to Stream Data
'''

class StreamListener(tweetpy.StreamListener):
    '''
    Stream Listener
    Overriden to Add Logic to on_status
    '''

    def on_status(self, status):
        print(status)