from pymongo import MongoClient

'''
Author: Ankit Kumar
DB API to Interface with the DB
The DB is NoSQL (MongoDB)
Defines SCRUD Functions and Schemas for Collections
'''

class TweetDB:
    '''
    Database API Class
    '''

    def __init__(self, logger):
        # Initialize DB Class
        self.logger = logger
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

        self.authors = self.db['authors']
        if self.authors is None:
            self.logger.debug("Cannot Find Collection for Authors!")

    # Tweets
    def add_tweet(self, data):
        # Add a new Tweet
        self.tweets.insert_one(data)

    def get_tweets(self, count):
        # Get 'N' Tweets
        self.logger.debug("Fetching %d Tweets" % (count,))

        data = self.tweets.find().sort("date", 1)
        size = len(data)
        if count < size:
            count = size
        
        if count == 0:
            self.logger.warning("Fetching Zero Tweets!")
        return data[:count]

    # Authors
    def add_author(self, data):
        # Add a new Author
        self.logger.debug("Adding a new Author")
        self.authors.insert_one(data)

    def get_author(self, id):
        # Get Author's Data
        self.logger.debug("Fetching Author (%d) Info" % (id,))

        data = self.authors.find({"id" : id})
        if data is None:
            self.logger.warning("Author (%d) Not Found" % (id,))
        return data