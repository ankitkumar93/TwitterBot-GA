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

        config = json.load(open(args.config))
        
        # Setup Stream Listener
        streamListener = StreamListener()
        streamListener.setup(dict(logger=args.logger, stream_path=config['stream_path'], tags_path=config['tags_path']))

        # Setup Stream
        key = json.load(open(config['key_path']))
        users = json.load(open(config['user_path']))
        auth = tweepy.OAuthHandler(key['consumer_key'], key['consumer_secret'])
        auth.set_access_token(key['access_token'], key['access_secret'])

        self.stream = tweepy.Stream(auth, streamListener)

    def fetch(self):
        self.stream.filter(languages=['en'], locations=[-180,-90,180,90])
        self.logger.debug("Starting To Stream!")


def fetch_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetFetch = TweetFetch(args)
    tweetFetch.fetch()