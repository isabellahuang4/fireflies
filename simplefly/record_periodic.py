#similarity score respects periodicity by finding common substring "wrapped"

import sys
import random as r
from statistics import mean
from periodic import Firefly
import csv

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 20
EPOCHS = 1000
PERTURB_PROB = .3
MUTATE_PROB = .1 
REPEATS = 20
    
def run_simulation(fireflies):
    for epoch in range(EPOCHS):
        r.shuffle(fireflies)

        for f in range(NUM_EACH):
            i = 2*f
            j = i+1
            same = fireflies[i].same_species(fireflies[j])
            #same species
            if same:
                #both no pattern
                if fireflies[i].pattern == None and fireflies[j].pattern == None:
                    fireflies[i].init_pattern()
                    fireflies[j].pattern = fireflies[i].pattern
                #j has pattern
                elif fireflies[i].pattern == None:
                    fireflies[i].pattern = fireflies[j].pattern
                #i has pattern
                elif fireflies[j].pattern == None:
                    fireflies[j].pattern = fireflies[i].pattern
                #both have
                else:
                    #compare aggregate sim scores, replicate smaller one 
                    #when replicating, do so with chance of mutation
                    if fireflies[i].simscore <= fireflies[j].simscore:
                        fireflies[j].pattern = fireflies[i].pattern
                        if r.random() < MUTATE_PROB and epoch < 975:
                            fireflies[j].mutate()
                        fireflies[j].reset_simscore()
                    else:
                        fireflies[i].pattern = fireflies[j].pattern
                        if r.random() < MUTATE_PROB and epoch < 975:
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

def list_flies(flies):
    flies.sort()
    seen = {}
    for f in flies:
        if (str(f.pattern), f.species) not in seen:
            seen[(str(f.pattern), f.species)] = 1
        else:
            seen[(str(f.pattern), f.species)] += 1
    return seen

def print_csv(results):
    with open('results.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        
        for run in results.keys():
            row = [run]
            flies = results[run]
            row += flies
            
            writer.writerow(row)


def main(args):
    runs = {}
    for r in range(REPEATS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = Firefly(i)

        run_simulation(fireflies)
        runs[r] = list_flies(fireflies)

    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
 