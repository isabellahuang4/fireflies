#test simscore and push periodic

import sys
import random as r
import math
import csv 
from itertools import combinations
from statistics import mean

from shift_simscore import Firefly as shifty_fly
from commonsub_simscore import Firefly as subby_fly

LENGTH = 6
MAX_FLASH = 4
NUM_SPECIES = 3
NUM_EACH = 15
EPOCHS = 200 
MUTATE_PROB = .1
TRIALS = 15

#given list of fireflies, the epoch number, and whether we are nudging periodic
def round(fireflies, epoch, push):
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
                    if r.random() < MUTATE_PROB and epoch < 195:
                        if push and r.random() < .3:
                            j.push_periodic()
                        else:
                            j.mutate()
                    j.reset_simscore()
                else:
                    i.pattern = j.pattern
                    if r.random() < MUTATE_PROB and epoch < 195:
                        if push and r.random() < .3:
                            i.push_periodic()
                        else:
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
    seen = {}
    for f in flies:
        if (str(f.pattern), f.species) not in seen:
            seen[(str(f.pattern), f.species)] = 1
        else:
            seen[(str(f.pattern), f.species)] += 1

    score1 = flies[0].calc_similarity(flies[15])
    score2 = flies[0].calc_similarity(flies[31])
    score3 = flies[15].calc_similarity(flies[31])
    score = mean([score1, score2, score3])
    seen[score] = 1

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

    #shift
    print('shift')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)

        for epoch in range(EPOCHS):
            round(fireflies, epoch, False)

        runs[('shift',rep)] = list_flies(fireflies)

    #commonsub
    print('commonsub')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i)

        for epoch in range(EPOCHS):
            round(fireflies, epoch, False)

        runs[('commonsub', rep)] = list_flies(fireflies)

    #shift + push
    print('shifty push')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)

        for epoch in range(EPOCHS):
            round(fireflies, epoch, True)

        runs[('shift_push',rep)] = list_flies(fireflies)

    #commonsub + push
    print('subby push')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i)

        for epoch in range(EPOCHS):
            round(fireflies, epoch, True)

        runs[('commonsub_push', rep)] = list_flies(fireflies)


    print('printing')
    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))