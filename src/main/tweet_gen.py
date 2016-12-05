import json
import random

from apis.tweet import TweetHelper
from apis.tracery_api import TraceryHelper
from apis.emotion import EmotionHelper
from population.selector import Selector
from population.filter import Filter
from population.syntax import Syntax

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
        
        self.config = json.load(open(args.config))

        self.tweetHelper = TweetHelper(dict(logger=self.logger,
                                            key_path=str(self.config['key_path'])))
        self.traceryHelper = TraceryHelper(dict(logger=self.logger,
                                                grammar_path=str(self.config['grammar_path'])))
        self.emotionHelper = EmotionHelper(dict(logger=self.logger,
                                                emotion_path=str(self.config['emotion_path']),
                                                rating_path=str(self.config['rating_path'])))
        self.syntax = Syntax(dict(logger=self.logger))

        self.filter = Filter(dict(logger=self.logger, tweet_helper=self.tweetHelper,
                                  filter_threshold=self.config['filter_threshold']))
        self.selector = Selector(dict(logger=self.logger, game_count=self.config['game_count']))

    def generate(self):
        self.logger.debug("Starting Generation!")

        # Get Game
        self.logger.debug("Getting Data!")
        basicGames = self.selector.select()
        count, filteredGames = self.filter.filter_from_list(basicGames)
        index = random.randint(0, count - 1)
        gameInfo = filteredGames[index]

        # Get Game Info
        game_name = gameInfo['name']
        game_rating = gameInfo['rating']

        # Get Emotion
        emotion = self.emotionHelper.get_emotion(game_rating)

        # Get Grammar
        syntax = self.syntax.get_syntax()

        # Get Tweet
        self.logger.debug("Generating Tweet!")
        tweetToPost = self.traceryHelper.gen_sentence(dict(game_name=game_name,
                                                           emotion=emotion,
                                                           syntax=syntax))
	print(tweetToPost)

        # Post Tweet
        #self.logger.debug("Posting Tweet!")
        #self.tweetHelper.post_tweet(tweetToPost)

        # Done
        self.logger.debug("Tweet Generation Finished!")


def gen_tweets(args):
    tweetGenerator = TweetGenerator(args)
    tweetGenerator.generate()
