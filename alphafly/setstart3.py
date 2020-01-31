# try three species

import sys
import csv
import random as r
from statistics import mean
from math import floor
from alpha import Firefly

LENGTH = 10
NUM_SPECIES = 3
NUM_EACH = 20
EPOCHS = 651
PERTURB = 1
MUTATE_PROB = .15 

PATTERNS = [ [0, 1, 2, 8, 1], \
                 [0, 1, 2, 6, 2], \
                 [0, 1, 2, 4, 3], \
                 [0, 1, 2, 2, 4], \
                 [0, 1, 2, 0, 5], \
                 [0, 2, 3, 7, 1], \
                 [0, 2, 3, 4, 2], \
                 [0, 2, 3, 1, 3], \
                 [0, 2, 4, 6, 1], \
                 [0, 2, 4, 2, 2], \
                 [0, 3, 4, 6, 1], \
                 [0, 3, 4, 2, 2], \
                 [0, 3, 5, 5, 1], \
                 [0, 3, 5, 0, 2], \
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
    track = {} #dictionary of epoch: list of patterns

    for epoch in range(EPOCHS):
        r.shuffle(fireflies)

        for f in range(floor(NUM_EACH*NUM_SPECIES/2)):
            i = 2*f
            j = i+1
            same = fireflies[i].same_species(fireflies[j])
            #same species
            if same:
                #both no pattern
                if fireflies[i].pattern == None and fireflies[j].pattern == None:
                    fireflies[i].init_pattern()
                    fireflies[j].pattern = fireflies[i].pattern[:]
                #j has pattern
                elif fireflies[i].pattern == None:
                    fireflies[i].pattern = fireflies[j].pattern[:]
                #i has pattern
                elif fireflies[j].pattern == None:
                    fireflies[j].pattern = fireflies[i].pattern[:]
                #both have
                else:
                    #compare aggregate sim scores, replicate higher one 
                    #with probability simscore/length
                    #when replicating, do so with chance of mutation
                    if fireflies[i].simscore >= fireflies[j].simscore:
                        fireflies[j].pattern = fireflies[i].pattern[:]
                        if r.random() < MUTATE_PROB and epoch < 250:
                            fireflies[j].mutate()
                        fireflies[j].reset_simscore()
                    else:
                        fireflies[i].pattern = fireflies[j].pattern[:]
                        if r.random() < MUTATE_PROB and epoch < 250:
                            fireflies[i].mutate()
                        fireflies[i].reset_simscore()
            #diff species
            else:
                if fireflies[i].pattern == None:
                    fireflies[i].init_pattern()
                if fireflies[j].pattern == None:
                    fireflies[j].init_pattern()
                distance = fireflies[i].calc_similarity(fireflies[j])
                fireflies[i].update_simscore(distance)
                fireflies[j].update_simscore(distance)
            
        if epoch % 50 == 0 and epoch != 0:
            track[epoch] = list_flies(fireflies)
    
    return track
            
def print_csv(results):
    with open('results.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')

        for pairing in results.keys():
            row = [pairing]
            for i in range(len(pairing)):
                row.append(PATTERNS[pairing[i]][1:5])
            epochs = results[pairing]
            row += epochs[650]

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
            for k in range(j+1, len(PATTERNS)):
                p = [PATTERNS[i], PATTERNS[j], PATTERNS[k]]
                results[(i, j, k)] = run_simulation(p)
    
    print_csv(results)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
