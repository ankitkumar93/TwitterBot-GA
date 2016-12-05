from pymongo import MongoClient
import random

'''
Author: Ankit Kumar
DB API to Interface with the DB
The DB is NoSQL (MongoDB)
Defines SCRUD Functions and Schemas for Collections
'''

class DBHelper:
    '''
    Database API Class
    '''

    def __init__(self, args):
        # Initialize DB Class
        self.logger = args['logger']
        self.logger.debug("Initializing DB API!")
        
        self.client = MongoClient('mongodb://localhost:27017')
        if self.client is None:
            self.logger.debug("Cannot connect to MongoDB!")

        self.db = self.client['tweet_ga']
        if self.db is None:
            self.logger.debug("Cannot Find Database!")

        self.tweets = self.db['tweets']
        if self.tweets is None:
            self.logger.debug("Cannot Find Collection for Tweets!")

        self.filtered_tweets = self.db['filtered_tweets']
        if self.tweets is None:
            self.logger.debug("Cannot Find Collection for Filtered Tweets!")

        self.syntax = self.db['syntax']
        if self.syntax is None:
            self.logger.debug("Cannot Find Collection for Syntaxses!")

        self.games = self.db['games']
        if self.games is None:
            self.logger.debug("Cannot Find Collection for Games!")

    # Tweets
    def add_tweet(self, data):
        # Add a new Tweet
        self.tweets.insert_one(data)

    def get_tweets(self, page, count):
        # Get 'N' Tweets
        self.logger.debug("Fetching %d Tweets" % (count,))
        data = self.tweets.find().skip(count*(page-1)).limit(count)
        return list(data)
        
    # Filtered Tweets
    def add_filtered_tweet(self, data):
        # Add a Filtered Tweets
        self.filtered_tweets.insert_one(data)


    def get_filtered_tweets_condition(self, lr_threshold):
        # Get 'N' Tweets (or All)
        data = self.filtered_tweets.find({"lrscore": {
                                            "$gte": lr_threshold}
                                         }).sort("lrscore")
        return list(data)

    def get_filtered_tweets(self):
        # Get 'N' Tweets (or All)
        data = self.filtered_tweets.find()
        return list(data)

    def update_filtered_tweet(self, tweetid, lrscore):
        # Updated a Filtered Tweet
        self.filtered_tweets.update_one({
            'tweetid': tweetid
            },{
                "$set": {
                    'lrscore': lrscore
                }
            }, upsert=False)

    # Syntax
    def add_syntax(self, data):
        # Add a new Syntax
        self.syntax.insert_one(data)

    def get_syntax(self):
        # Return Syntaxes
        syntaxes = self.syntax.find()
        return syntaxes

    def get_random_syntax(self):
        # Return a random row
        data = list(self.syntax.find())
        size = len(data)
        randomIndex = random.randint(0, size - 1)

        return data[randomIndex]

    # Games
    def get_games(self, count):
         # Get 'N' Games
        self.logger.debug("Fetching %d Games" % (count,))

        data = self.games.find().limit(count)
        return list(data)