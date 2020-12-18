#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
optinetd.py (Using DEAP)

Optimal design of networks using metaheuristics.
Layout and pipe size optimization of irrigation networks.

@author: Eduardo Jiménez Hernández
@email: eduardojh@email.arizona.edu
"""
#import csv
import random
import numpy as np
import pandas as pd
from datetime import datetime
from deap import base, creator, tools, algorithms
from hydraulic import Network, simulate_network
from objfun import pipe_price, network_diameters, index2diam, \
    test_network_cost
from plot import plot_convergence
random.seed()


def optimize_diameters(path, inpfile, **kwargs):
    """ Optimize diameters

    Optimize pipe diameters of a hydraulic network using Genetic Algorithms.

    :param str path: path to the input file.
    :param str inpfile: EPANET's input file (INP) with network data.
    :param int pop: population size or number of individuals.
    :param int gen: number of generations.
    :param float cxbp: crossover (mating) probability.
    :param float mutpb: mutation probability.
    :param float indpb: individual mutation probability?
    """

    _unit_price = kwargs.get('prices', {})
    _popsize = kwargs.get('pop', 200)
    _cxpb = kwargs.get('cxpb', 0.9)
    _mutpb = kwargs.get('mutpb', 0.02)
    _indpb = kwargs.get('indpb', 0.10)
    _generations = kwargs.get('gen', 500)

    # Create the appropiate types for diameter optimization
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Create the Network object needed for EPANET simulation and analysis
    network = Network(path, inpfile)
    network.open_network()
    network.initialize()

    # Create the individuals and population
    # dimension = network.links
    # individual size = network.links
    toolbox = base.Toolbox()
    toolbox.register("attr_diameter", random.randint, 0, len(_unit_price)-1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_diameter, network.links)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Genetic operators and evaluation function
    toolbox.register("evaluate", lambda x: network_diameters(x, network,
                                                             _unit_price))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=_indpb)
    toolbox.register("select", tools.selRoulette)

    # Create the population
    pop = toolbox.population(n=_popsize)
    hof = tools.HallOfFame(1)  # To remember best solution
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Use simplest evolutionary algorithm as in chapter 7 of Back (2000)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=_cxpb, mutpb=_mutpb,
                                   ngen=_generations, stats=stats,
                                   halloffame=hof, verbose=True)
    return hof, pop, log


def optimize_diameters_execs(path, inpfile, execs, **kwargs):
    """ Optimize diameters

    Optimize pipe diameters of a hydraulic network using Genetic Algorithms.
    
    Warning! This assumes single-objective optimization, so only the first
    element of the best solutions tuple is going to be used.

    :param str path: path to the input file.
    :param str inpfile: EPANET's input file (INP) with network data.
    :param int pop: population size or number of individuals.
    :param int gen: number of generations.
    :param float cxbp: crossover (mating) probability.
    :param float mutpb: mutation probability.
    :param float indpb: individual mutation probability?
    :param str dir: directory to save the results.
    :return best: a list of diameters (best solution)
    """

    start = datetime.now()

    _unit_price = kwargs.get('prices', {})
    _popsize = kwargs.get('pop', 200)
    _cxpb = kwargs.get('cxpb', 0.9)
    _mutpb = kwargs.get('mutpb', 0.02)
    _indpb = kwargs.get('indpb', 0.05)
    _generations = kwargs.get('gen', 500)
    _dir = kwargs.get('dir', 'results/')

    f = '%Y_%m_%d-%H_%M_%S'
    _stats = _dir + 'ga_dimen_' + datetime.strftime(start, f) + '.csv'
    _sol = _stats[:-4] + '.txt'

    best = None
    stats = pd.DataFrame(columns=['gen', 'nevals', 'avg', 'std', 'min', 'max', 'bestFit'])

    for i in range(execs):
        print('Execution {0} of {1} ...'.format(i+1, execs))

        b, p, r = optimize_diameters(path, inpfile, prices=_unit_price,
                                     pop=_popsize, cxpb=_cxpb, mutpb=_mutpb,
                                     indpb=_indpb, gen=_generations)
        if best is None:
            best = b.items[0]
        elif b.items[0].fitness.values[0] < best.fitness.values[0]:
            best = b.items[0]
        print("Best iter: ", best.fitness.values[0])
        # print("\nMy Dataframe\n")
        df = pd.DataFrame(r)
        df['bestFit'] = best.fitness.values[0]
        stats = stats.append(df)
            
    # Runtime
    runtime = datetime.now() - start
    print('Run time: {0} executions in {1}'.format(execs, runtime))
    
    # Save statistics to a text file
    # stats.to_csv(_stats)
    stats.to_csv(_stats, index=False)
    
    # Plot the convergence chart
    plot_convergence(execs, _generations, _stats)

    # Save best solution to a text file
    with open(_sol, 'a') as f:
        f.write('Best solution:\t{0}\n'.format(best))
        f.write('Best fitness:\t{0}\n'.format(best.fitness.values[0]))
        f.write('Run time:\t{0}'.format(runtime))

    return best


if __name__ == "__main__":
    ## TEST 1: Simulate a network using EPANET Toolkit
    path = '../data/'
    inpfile = 'TwoLoop.inp'
    # test_network_cost(path, inpfile)
    # simulate_network(path, inpfile)
    ## END OF TEST 1
    
    ## TEST 2: Optimization
    # Read the pipe prices from Alperovits & Shamir (1977)
    # Two loop network cost: 497,525
    pipeprice = pipe_price('../data/pipe_cost_Aperovits_Shamir_1977_mm.csv')

    # b, p, r = optimize_diameters(path, inpfile, prices=pipeprice, gen=100)
    # best = b[0]
    # ## END OF TEST 2
    
    # ## TEST 3: Optimize the diameters

    # # Run several executions of the Genetic Algorithm to optimize diameters
    # # execs = 1  #  Start with one execution and see how long it takes
    execs = 3  #  Do several executions to
    best = optimize_diameters_execs(path, inpfile, execs, prices=pipeprice,
                                    mutpb=0.1, gen=10, dir='../results/',
                                    pop=200)

    # Perform a simulation of the network with the best solution obtained
    network = Network(path, inpfile)
    network.open_network()
    network.initialize()

    # Show the results
    print("*" * 40)
    print("Minimal cost:\t{0}".format(network_diameters(best, network,
          pipeprice)))
    print("*" * 40)
    network.close_network()
    simulate_network(path, inpfile, diameters=index2diam(best, pipeprice))
    # ## END OF TEST 3