import tweepy
import json
from apis.streamer import StreamListener

'''
Author: Ankit Kumar
Tweet Fetcher Module
Streams Tweets and Stores Them in the DB
Only Streams Tweets Related to Video Games
'''

class TweetFetch:
    '''
    Tweet Fetcher Class
    '''

    def __init__(self, args):
        self.logger = args.logger
        self.logger.debug("Setting Up Stream!")
        
        streamListener = StreamListener()
        key = json.load(open(args.keyPath))
        users = json.load(open(args.userPath))
        auth = tweepy.OAuthHandler(key['consumer_key'], key['consumer_secret'])
        auth.set_access_token(key['access_token'], key['access_secret'])

        self.users = [users['ign'], users['ytgaming'], users['twitch'], users['gamespot']]
        self.stream = tweepy.Stream(auth, streamListener)

    def fetch(self):
        self.stream.filter(follow=self.users)
        self.logger.debug("Starting To Stream!")


def fetch_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetFetch = TweetFetch(args)
    tweetFetch.fetch()