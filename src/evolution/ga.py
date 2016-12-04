from apis.db import DBHelper
from ga_operators import GAOperators
import json
import random

'''
Author: Ankit Kumar
Genetic Algorithm: Defines the Genetic Algorithm
'''

class GeneticAlgorithm:
    def __init__(self, args):
        self.logger = args['logger']
        config = json.load(open(args['config']))
        self.gaoperators = GAOperators(dict(individualLength=config['individual_length'],
                                            crossoverPoint=config['crossover_point'],
                                            crossoverProbability=config['crossover_probability'],
                                            mutationProbability=config['mutation_probability'],
                                            numElite=config['num_elite']))
        self.lrThreshold = config['lr_threshold']
        self.maxFitness = config['max_fitness']
        self.maxIterations = config['max_iterations']
        self.populationSize = config['population_size']
        self.goalPopulationSize = args['goal_population_size']
        self.numElite = config['num_elite']

        self.db = DBHelper(dict(logger=args['logger']))

    def generate_population(self):
        data = self.db.get_filtered_tweets()
        random.shuffle(data)
        self.population = data[:self.populationSize]


    def generate_goal_population(self):
        goalData = self.db.get_filtered_tweets_condition(self.lrThreshold)
        random.shuffle(goalData)
        goalPopulation = goalData[:self.goalPopulationSize]
        self.gaoperators.set_goal_population(goalPopulation)
        

    def evolve(self):
        for gen in range(self.maxIterations):
            self.logger.debug("--Generations: %d--" % gen)

            # Compute Fitness
            for individual in self.population:
                self.gaoperators.evaluate(individual)

            fittestChild = max(self.population, key=lambda child: child.fitness)
            if fittestChild.fitness >= self.maxFitness:
                break

            # Generate Offsprings
            # Select Elites
            offsprings = self.gaoperators.select(self.population)

            # CrossOver
            remainingOffsprings = self.populationSize - self.numElite
            while remainingOffsprings > 0:
                    childIndex = random.sample(xrange(numElite - 1), 2)
                    child1 = offsprings[childIndex[0]]
                    child2 = offsprings[childIndex[1]]

                    offspring1 , offspring2 = self.gaoperators.crossover(child1, child2)
                    offsprings.append(offspring1)
                    offsprings.append(offspring2)

                    remainingOffsprings -= 2

            # Mutation
            for childIndex in xrange(numElite, self.populationSize - 1):
                child = offsprings[childIndex]
                self.gaoperators.mutate(child)

            # Set Population to new Generation
            self.population[:] = offsprings

        solution = max(self.population, key=lambda child: child.fitness)
        return solution
