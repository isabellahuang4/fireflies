#similarity score respects periodicity by finding common substring "wrapped"

import sys
import random as r
from statistics import mean
from multiple_periodic import Firefly
from multiple_periodic import other_species
import csv

LENGTH = 10
NUM_SPECIES = 3
NUM_EACH = 20
EPOCHS = 2000
PERTURB_PROB = .3
MUTATE_PROB = .1 
REPEATS = 50

    
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
                    focus = r.choice(other_species(fireflies[i].species))

                    if fireflies[i].simscore[focus] <= fireflies[j].simscore[focus]:
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
                fireflies[i].update_simscore(distance, fireflies[j].species)
                fireflies[j].update_simscore(distance, fireflies[i].species)

def list_flies(flies):
    flies.sort()
    seen = {}
    for f in flies:
        if (str(f.pattern), f.species) not in seen:
            seen[(str(f.pattern), f.species)] = 1
        else:
            seen[(str(f.pattern), f.species)] += 1

    #assume has converged, get simscores
    a = flies[0].calc_similarity(flies[NUM_EACH + 1])
    print(a)
    b = flies[NUM_EACH +1].calc_similarity(flies[NUM_EACH*2 + 2])
    print(b)
    c = flies[0].calc_similarity(flies[NUM_EACH*2 + 2])
    print(c)
    seen[a] = (1,2)
    seen[b] = (2,3)
    seen[c] = (1,3)
    return seen


def print_csv(results):
    with open('results_multiple.csv', mode = 'w') as file:
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
 
