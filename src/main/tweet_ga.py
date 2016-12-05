import json
from evolution.ga import GeneticAlgorithm
from apis.db import DBHelper

'''
Author: Ankit Kumar
Genetic Algorithm for Tweets
Optimizes Tweet Structure using Genetic Algorithm
'''

class TweetGA:
    '''
    Genetic Algorithm
    '''

    def __init__(self, args):
        self.logger = args.logger
        config = json.load(open(args.config))
        self.ga = GeneticAlgorithm(dict(logger=args.logger, ga_path=config['ga_path'], goal_population_size=args.goal))
        self.db = DBHelper(dict(logger=args.logger))

    def run(self):
        self.logger.debug("Starting Evolution!")
        self.ga.generate_population()
        self.ga.generate_goal_population()
        solution = self.ga.evolve()

        # Check for Invalid Solution
        assert solution, 'Invalid solution!'

        self.logger.debug("--Solution: Fitness: %d, Syntax: %s--"
                          % (solution['fitness'], solution['tags']))

        self.db.add_syntax(dict(data=solution['tags']))


def ga_tweets(args):
    tweetGA = TweetGA(args)
    tweetGA.run()
