# two species
# just calc simscores
# with relaxed alpha characterisation

import sys
import csv
import random as r
from statistics import mean
from math import floor
from relaxed import Firefly

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 1
MUTATE_PROB = .15 

PATTERNS = [ [0, 1, 2, 0, 1], \
                 [0, 1, 2, 1, 1], \
                 [0, 1, 2, 2, 1], \
                 [0, 1, 2, 3, 1], \
                 [0, 1, 2, 4, 1], \
                 [0, 1, 2, 5, 1], \
                 [0, 1, 2, 6, 1], \
                 [0, 1, 2, 7, 1], \
                 [0, 1, 2, 8, 1], \
                 [0, 1, 2, 0, 2], \
                 [0, 1, 2, 1, 2], \
                 [0, 1, 2, 2, 2], \
                 [0, 1, 2, 3, 2], \
                 [0, 1, 2, 4, 2], \
                 [0, 1, 2, 5, 2], \
                 [0, 1, 2, 6, 2], \
                 [0, 1, 2, 0, 3], \
                 [0, 1, 2, 1, 3], \
                 [0, 1, 2, 2, 3], \
                 [0, 1, 2, 3, 3], \
                 [0, 1, 2, 4, 3], \
                 [0, 1, 2, 0, 4], \
                 [0, 1, 2, 1, 4], \
                 [0, 1, 2, 2, 4], \
                 [0, 1, 2, 0, 5], \
                 [0, 2, 3, 0, 1], \
                 [0, 2, 3, 1, 1], \
                 [0, 2, 3, 2, 1], \
                 [0, 2, 3, 3, 1], \
                 [0, 2, 3, 4, 1], \
                 [0, 2, 3, 5, 1], \
                 [0, 2, 3, 6, 1], \
                 [0, 2, 3, 7, 1], \
                 [0, 2, 3, 0, 2], \
                 [0, 2, 3, 1, 2], \
                 [0, 2, 3, 2, 2], \
                 [0, 2, 3, 3, 2], \
                 [0, 2, 3, 4, 2], \
                 [0, 2, 3, 0, 3], \
                 [0, 2, 3, 1, 3], \
                 [0, 2, 4, 0, 1], \
                 [0, 2, 4, 1, 1], \
                 [0, 2, 4, 2, 1], \
                 [0, 2, 4, 3, 1], \
                 [0, 2, 4, 4, 1], \
                 [0, 2, 4, 5, 1], \
                 [0, 2, 4, 6, 1], \
                 [0, 2, 4, 0, 2], \
                 [0, 2, 4, 1, 2], \
                 [0, 2, 4, 2, 2], \
                 [0, 3, 4, 0, 1], \
                 [0, 3, 4, 1, 1], \
                 [0, 3, 4, 2, 1], \
                 [0, 3, 4, 3, 1], \
                 [0, 3, 4, 4, 1], \
                 [0, 3, 4, 5, 1], \
                 [0, 3, 4, 6, 1], \
                 [0, 3, 4, 0, 2], \
                 [0, 3, 4, 1, 2], \
                 [0, 3, 4, 2, 2], \
                 [0, 3, 5, 0, 1], \
                 [0, 3, 5, 1, 1], \
                 [0, 3, 5, 2, 1], \
                 [0, 3, 5, 3, 1], \
                 [0, 3, 5, 4, 1], \
                 [0, 3, 5, 5, 1], \
                 [0, 3, 5, 0, 2], \
                 [0, 3, 6, 0, 1], \
                 [0, 3, 6, 1, 1], \
                 [0, 3, 6, 2, 1], \
                 [0, 3, 6, 3, 1], \
                 [0, 3, 6, 4, 1] ]
    
def create_fireflies(p):
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)
            fireflies[j+(NUM_EACH*i)].pattern = p[i]
    return fireflies

#input: all flies in simulation
#returns dictionary with [a_pattern, species]: frequency in population
def list_flies(flies):
    flies.sort()
    seen = {}
    for f in flies:
        if (str(f.pattern[1:5]), f.species) not in seen:
            seen[(str(f.pattern[1:5]), f.species)] = 1
        else:
            seen[(str(f.pattern[1:5]), f.species)] += 1
    return seen

#p is LIST of start patterns for each species
def run_simulation(p):
    fireflies = create_fireflies(p)
    s1 = fireflies[0].calc_similarity(fireflies[1])
    return [s1]
            
def print_csv(results):
    with open('results.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')

        for pairing in results.keys():
            row = [pairing]
            for i in range(len(pairing)):
                row.append(PATTERNS[pairing[i]][1:5])
            scores = results[pairing]
            row += scores

            writer.writerow(row)

            #epochs = results[pairing]
            #for e in epochs.keys():
                #line = [e]
                #line += epochs[e].items()
                #writer.writerow(line)
            


def main(args):
    results = {}
    #do every possible first pairing, save the final results
    for i in range(len(PATTERNS)):
        for j in range(i+1, len(PATTERNS)):
            p = [PATTERNS[i], PATTERNS[j]]
            results[(i, j)] = run_simulation(p)
    
    print_csv(results)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
