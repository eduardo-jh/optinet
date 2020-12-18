#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
objfun.py

This file has some obective functions for:
    1) Finding the optimal pipe diameter for water distribution systems
    2) Finding the optimal layout for water distribution systems
    3) Some utility functions (read prices, conversions, etc.)

NOTE:
In the futture, multiple diameter values on the same pipe segment (a connection
between two junctions) should be alowed.

@author: Eduardo Jiménez Hernández
@email: eduardojh@email.arizona.edu
"""
import csv
import random
from hydraulic import Network, simulate_network

random.seed()


# ***** ***** Uility functions ***** *****


def pipe_price(filename):
    """ Pipe price

    Reads the pipe prices from a CSV text file. Each price corresponds to a
    pipe diameter (in milimeters, inches, etc.) for each unit of length (meter,
    foot, etc.).

    :param str filename: the path and name of the file containing the prices
    """
    with open(filename, 'r') as f:
        csvreader = csv.reader(f)
        cost = {}
        for row in csvreader:
            assert len(row) == 2, "Incorrect number of columns in file"
            k, v = int(row[0]), int(row[1])
            cost[k] = v
    return cost


def index2diam(diam_indexes, pipe_price):
    """ Index to diameter

    Get the diameter in real dimensions (milimeters, inches, etc.) from the
    keys of a dictionary with the pipe costs using its position.

    :param list diam_indexes: a list with the diameter indexes
    :param dict pipe_price: dictionary with unit prices of each pipe diameter
    :return list diameters: the pipe diameters in real dimensions
    """
    keys = sorted(pipe_price.keys())
    # List of real diameters of the network's pipes
    d = [keys[x] for x in diam_indexes]
    return d


def test_network_cost(path, inpfile):
    """ Test network cost
    
    A simple function to test some parameters of an EPANET's network simulation
    """
    network = Network(path, inpfile)
    network.open_network()
    network.initialize()
    # diameters_in = [18, 10 ,16, 4, 16, 10, 10, 1]
    diam = [457, 254, 406, 102, 406, 254, 254, 25]  # Best known
    # diam = [457, 305, 559, 102, 559, 305, 25, 305]  # Yet another solution

    print(network_cost(diam, network, pipeprice, vmin=0.3))

    simulate_network(path, inpfile, diameters=diam)


# ***** ***** Initialize population diameters ***** *****


def init_diam(x, dimension, prices):
    """ Init diameters

    An initialization function for the diameters optimization, creates a random
    population.

    :param list x: list of indices of pipe diameters
    :param int dimension: problem dimension (number of pipes in the network)
    :param dict prices: dictionary with unit prices of each pipe diameter
    :return list x: a list of real diameters (mm, in)
    """
    diameters = sorted(prices.keys())
    # diameters.sort()
    for i in range(dimension):
        x.append(diameters[random.randrange(0, len(diameters))])
    # print(x.genomeList)
    return x


# ***** ***** Optimal diameters ***** *****


def network_cost(diameters, network, unit_prices, **kwargs):
    """" The objective function for dimensioning optimization

    WARNING: This diameters should be in the real dimensions (milimeters,
    inches, etc.), and Epanet will handle it properly

    :param object network: an implementation of a 'Network' class
    :param list diameters: a list of pipe diameters (mm, in)
    :param dict unit_prices: a dictionary of unit prices for each diameter
    :return float fitness: minimum is better
    """
    _hmin = kwargs.get('hmin', 30.0)
    _hmax = kwargs.get('hmax', 100.0)
    _vmin = kwargs.get('vmin', 0.25)
    _vmax = kwargs.get('vmax', 2.50)
    _penalty = kwargs.get('penalty_step', 1)

    # Perform the EPANET simulation
    network.change_diameters(diameters)
    network.simulate()

    # Penalty for violating the pressure head constraints at each node
    pH = 1
    for i in range(network.nodes):
        # Ignore source nodes in pressure analysis
        # In EPANET source nodes=1 and consumer nodes=0
        if network.sources[i] == 0:
            if network.pressure[i] < _hmin or network.pressure[i] > _hmax:
                pH += _penalty

    # Penalty for violating the flow velocity constraints of the pipes
    pV = 1
    for i in range(network.links):
        if network.velocity[i] < _vmin or network.velocity[i] > _vmax:
            pV += _penalty

    # Objective function
    cost = 0
    for i in range(len(diameters)):
        c = unit_prices[diameters[i]] * network.lengths[i] * pV * pH
        cost += c
    return cost


def network_diameters(diam_indexes, network, pipe_price):
    """ Network diameters

    Assings real pipe diameters from a list of indexes and calculates
    the cost of the network using such diameters.

    :param list diam_indexes: the indexes of the pipe diameters
    :param network: a Network instance
    :param dict pipe_price: dictionary with unit prices of each pipe diameter
    """
    diameters = index2diam(diam_indexes, pipe_price)
    # Return the cost of the network
    # IMPORTANT: This should return a tuple, according to fitness weights
    # notice the trailing comma
    return network_cost(diameters, network, pipe_price),


if __name__ == "__main__":
    # Read the pipe prices
    # pipe_cost.csv from Alperovits & Shamir (1977)
    # Two loop network cost: 497,525

    pipeprice = pipe_price('../data/pipe_cost_Aperovits_Shamir_1977_mm.csv')

    # Test 1: Simulate a network
    path = '../data/'
    inpfile = 'TwoLoop.inp'

    test_network_cost(path, inpfile)
