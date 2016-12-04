import json
from evolution.ga import GeneticAlgorithm

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

    def run(self):
        self.ga.generate_population()
        self.ga.generate_goal_population()
        self.ga.evolve()

def tweets_ga(args):
    tweetGA = TweetGA(args)
    tweetGA.run()

