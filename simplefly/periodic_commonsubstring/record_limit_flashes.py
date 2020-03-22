#record results 
#use to play with different length/flash ratios, should be around 4:10 or 5:10

import sys
import random as r
from statistics import mean
from itertools import combinations
#from limit_flashes import Firefly
from set_flashes import Firefly
import csv

NUM_SPECIES = 10
NUM_EACH = 10
EPOCHS = 350
MUTATE_PROB = .1 
REPEATS = 10
    
def run_simulation(fireflies):
    for epoch in range(EPOCHS):
        r.shuffle(fireflies)

        for (i, j) in combinations(fireflies, 2):
            same = i.same_species(j)
            #same species
            if same:
                #both no pattern
                if i.pattern == None and j.pattern == None:
                    i.init_pattern()
                    j.pattern = i.pattern
                #j has pattern
                elif i.pattern == None:
                    i.pattern = j.pattern
                #i has pattern
                elif j.pattern == None:
                    j.pattern = i.pattern
                #both have
                else:
                    #compare aggregate sim scores, replicate smaller one 
                    #when replicating, do so with chance of mutation
                    if i.simscore <= j.simscore:
                        j.pattern = i.pattern
                        if r.random() < MUTATE_PROB and epoch < 325:
                            j.mutate()
                        j.reset_simscore()
                    else:
                        i.pattern = j.pattern
                        if r.random() < MUTATE_PROB and epoch < 325:
                            i.mutate()
                        i.reset_simscore()
            #diff species
            else:
                if i.pattern == None:
                    i.init_pattern()
                if j.pattern == None:
                    j.init_pattern()
                distance = i.calc_similarity(j)
                i.update_simscore(distance)
                j.update_simscore(distance)

def list_flies(flies):
    flies.sort()
    scores = {}
    running = []
    seen = {}
    for f in flies:
        if (str(f.pattern), f.species) not in seen:
            seen[(str(f.pattern), f.species)] = 1
            for fire in running:
                scores[f.calc_similarity(fire)] = 1
            running.append(f)
        else:
            seen[(str(f.pattern), f.species)] += 1
    print(scores)
    seen.update(scores)
    return seen

def print_csv(results):
    with open('results_set_flash.csv', mode = 'w') as file:
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
 
