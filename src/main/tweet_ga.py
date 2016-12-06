import json
from evolution.ga import GeneticAlgorithm
from apis.db import DBHelper
from apis.syntax_gen import SyntaxGen

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
        self.syntaxgen = SyntaxGen(dict(logger=args.logger, sg_path=config['sg_path']))

    def run(self):
        self.logger.debug("Starting Evolution!")

        # Generate Population
        self.ga.generate_population()

        # Generate Goal Population (For Comparison)
        self.ga.generate_goal_population()

        # Run Evolution
        solution = self.ga.evolve()

        # Check for Invalid Solution
        assert solution, 'Invalid solution!'

        self.logger.debug("Solution: Fitness: %f, Syntax: %s"
                          % (solution['fitness'], solution['tags']))

        # Convert Tags to a Syntax (String)
        solutionSyntax = self.syntaxgen.create_syntax(solution['tags'])

        # Add Syntax to DB
        self.db.add_syntax(dict(data=solutionSyntax))


def ga_tweets(args):
    tweetGA = TweetGA(args)
    tweetGA.run()
