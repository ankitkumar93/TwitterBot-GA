import json

from apis.tweet import TweetHelper
from apis.tracery_api import TraceryHelper
from population.selector import Selector
from population.filter import Filter

'''
Author: Ankit Kumar
Tweet Generator
Selects a Game and a Grammar
Uses tracery to Generate the Tweet
'''

class TweetGenerator:
    '''
    Tweet Generator API
    '''
    def __init__(self, args):
        self.logger = args.logger
        self.logger.debug("Initializing Tweet Generator!");

        config = json.load(open("config.json"));

        self.tweetHelper = TweetHelper(dict(logger=self.logger, keyPath=config.key_path))
        self.filter = Filter(dict(logger=self.logger, tweetHelper=tweetHelper, filterThreshold=config.filter_threshold))
        self.selector = Selector(dict(logger=self.logger))
        self.traceryHelper = TraceryHelper(dict(logger=self.logger))

    def generate(self):
        self.logger.debug("Starting Generation!")

        # Get Game
        self.logger.debug("Getting Game!")
        basicGames = self.selector.select(config.games_selection_count)
        count, filteredGames = self.filter.filter_from_list(basicGames)
        index = random.randInt(0, count - 1)
        gameInfo = filteredGames[index]
        
        # Get Tweet
        self.logger.debug("Generating Tweet!")
        tweetToPost = self.traceryHelper(gameInfo)

        # Post Tweet
        self.logger.debug("Posting Tweet!")
        self.tweetHelper.post_tweet(tweetToPost)

        # Done
        self.logger.debug("Tweet Generation Finished!")



def gen_tweets(args):
    tweetGenerator = TweetGenerator(args)
    tweetGenerator.generate()
    