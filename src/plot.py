#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create plots for the optimization

@author: Eduardo Jiménez Hernández
@email: eduardojh@email.arizona.edu
"""
import csv
import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

def plot_convergence(runs, gens, file_stats):
    """ Creates a convergence chart

    Plot the fitness of each generation to create a convergence chart, using
    the data saved in the statistics file created by the evolution.

    :param int runs: number of executions or runs
    :param int gens: generations of each execution
    :param str file_stats: CSV file containing data from evolution
    """

    # Read the data from CSV file, the format is as follow
    # column 0: gen,
    # column 1: nevals,
    # column 2: avg,
    # column 3: std,
    # column 4: min,
    # column 5: max
    # column 6: bestFit
    COL_GEN = 0
    COL_MIN = 6

    # Create the figure
    figConvergence = plt.figure()

    # Read all the data from the file
    gen = []
    rmin = []

    with open(file_stats, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            gen.append(int(row[COL_GEN]))      # Generation
            rmin.append(float(row[COL_MIN]))   # Raw minimum

    # print(gen)
    
    # Get the data slicing through executions, each run contains all its
    # generations and fitness
    ini = 0
    end = gens+1  # DEAP Adds +1 generations
    best = rmin[ini:end]
    g = gen[ini:end]
    print(g)

    # Get the best of each generation
    for r in range(runs):
        y = rmin[ini:end]
        for i in range(len(y)):
            if y[i] < best[i]:
                best[i] = y[i]
        ini += gens+1  # DEAP Adds +1 generations
        end += gens+1  # DEAP Adds +1 generations
    
    # Annotate
    plt.axhline(y=best[-1], linestyle='-.', color='gray', alpha=0.8,
                linewidth=0.8)
    plt.xlim(0, g[-1])
    
    # Plot the data: generation vs best fitness
    plt.plot(g, best, c='black')

    # Remove excess of tick marks and add the best solution
    loc, lab = plt.yticks()
    # print(loc)
    nloc = [i for i in loc if i >= best[-1]]
    nloc.sort()
#    if len(nloc) > 5:
#        del nloc[1::2]
    if (nloc[0]-best[-1]) < 50000:
        del nloc[0]
    nloc.insert(0, best[-1])
    plt.yticks(nloc)

    # Use scientific notation in y-axis
#    tick_spacing = (max(loc) - min(loc))/4
#    f = ticker.ScalarFormatter(useOffset=False, useMathText=True)
#    g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
#    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(g))
#    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    
    # Put titles to the figure
    plt.title('Convergence chart for {0} executions.'.format(runs))
    plt.xlabel('Generation')
    plt.ylabel('Cost')
    
    # Create a new file with PNG extension to save the chart
    file_fig = file_stats[:-4]
    file_fig = file_fig + ".png"

    plt.savefig(file_fig, bbox_inches='tight', dpi=300, transparent=True)
    figConvergence.show()
