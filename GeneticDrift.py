#!/usr/bin/env python3
"""
Script to simulate genetic drift via 1D random walk (Python programming exercise)
Author: Thanh Tan Huynh Huu
Created: 23 April 2023
"""

# Import necessary modules

import numpy as np
import matplotlib.pyplot as plt
import random
import argparse

# Setup for command line execution of script

parser = argparse.ArgumentParser(
                    prog='GeneticDriftSimulation',
                    description='This script simulates genetic drift based on population/step size and generation time',
                    epilog='Output: .png file in the same directory as the script')

parser.add_argument('--pop', type=int, required=True, help='population size [int]')
parser.add_argument('--subpop', type=int, required=True, help='number of subpopulations [int], it should be a divisor of chosen population size')
parser.add_argument('--gen', type=int, required=True, help='generation limit [int]')
parser.add_argument('--step', type=int, required=True, help='step size [int]')
args = parser.parse_args()

# Parameters

pop = args.pop
subpop = args.subpop
step_size = args.step
generation_limit = args.gen

# Function to simulate genetic drift, returns 1 array for generation time and 1 2D array to show frequencies of subpopulations

def genwalk(steps=1000,stepsize=1,population=100, subpopulation=10):
    # List comprehension creates reusable time axis for plotting 
    gens = np.array([i for i in range(0,steps)])
    # Create nested 2D list, every list within represents allele frequencies of a subpopulation
    genlist = []
    # Set initial frequency value at 50 %
    for j in range(0,subpopulation):
        if population % 2 != 0:
            genlist.append([int(round(population/2,0))])
        else:
            genlist.append([int(population/2)])
    
    # Append and add step sizes to initial elements over every new generation 
    for i in range(1,steps):
        # Create a list in which every subpopulation (lists within 2D list) gets randomly assigned a value, ensuring constant overall frequency 
        choice_a = int(subpopulation/2)*[stepsize]
        choice_b = int(subpopulation/2)*[-stepsize]
        choicelist = choice_a + choice_b
        random.shuffle(choicelist)
        # Append step sizes to subpopulation lists
        for k in range(0,subpopulation):
            nest_list = genlist[k]
            # If allele frequency reaches 0 % or 100 %, the graph remains fixed
            if 0 in nest_list:
                nest_list.append(0)
            elif population in genlist[k]:
                nest_list.append(population)
            # Step size is added 
            else:
                next_element = nest_list[i-1] +choicelist[k]
                nest_list.append(next_element)
    # Absolute values in lists converted to percentages relative to subpopulation size within 2D array
    genlist = np.array(genlist)/population*100
    return(gens,genlist)

# Create and save genetic drift plot in working directory

plt.figure()
# Iterate through 2D array sublists to show subpopulation frequencies in one plot
for i in range(0,subpop):
    plt.plot(genwalk(steps=generation_limit, stepsize=step_size, population = pop/subpop, subpopulation=subpop)[0],genwalk(steps=generation_limit, stepsize=step_size, population = pop/subpop, subpopulation=subpop)[1][i])
plt.xlim(0,)
plt.title('Genetic drift of '+ str(subpop) +' subpopulations, total population size: ' + str(pop))
plt.xlabel('Generation')
plt.ylabel('Allele frequency within subpopulation [%]')
plt.savefig('Genetic_Drift_Simulation.png')
plt.close()
