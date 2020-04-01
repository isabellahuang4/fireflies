#test exponential v regular simscore -- longest common substring
#second test: twostep game v regular game 
#      two step game HAS different species flies comparing simscores normally***

import sys
import random as r
import math
import csv 
from itertools import combinations
from statistics import mean

from exponential import Firefly as exp_fly
from commonsub_simscore import Firefly as subby_fly

LENGTH = 6
MAX_FLASH = 4
NUM_SPECIES = 3
NUM_EACH = 15
EPOCHS = 500 
MUTATE_PROB = .1
DECISION_THRESHOLD = .7
PENALTY = -20
REWARD = 10 
TRIALS = 10

#given list of fireflies, the epoch number, and whether we are nudging periodic
def round_one(fireflies, epoch, push):
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
                    if r.random() < MUTATE_PROB and epoch < 475:
                        if push and r.random() < .3:
                            j.push_periodic()
                        else:
                            j.mutate()
                    j.reset_simscore()
                else:
                    i.pattern = j.pattern
                    if r.random() < MUTATE_PROB and epoch < 475:
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


def round_two(fireflies):
    r.shuffle(fireflies)
    for (i,j) in combinations(fireflies, 2):
        #i sends partial sequence
        start = r.randint(0, LENGTH-4) #note we're picking indices
        end = r.randint(start+3, LENGTH-1) #ensure that seq is at least 3 long
        seq_length = end-start
        seq = i.pattern[start:end]
        #j makes decision based on substring match with j's full pattern
        decision = j.make_decision(seq)
        if decision < DECISION_THRESHOLD:
            #decided different species
            if i.same_species(j):
                #neg penalty
                i.update_score(PENALTY*(seq_length/LENGTH))
                j.update_score(PENALTY*(seq_length/LENGTH))
            else:
                #pos reward 
                i.update_score(REWARD*(LENGTH/seq_length))
                j.update_score(REWARD*(LENGTH/seq_length))
        else:
            #decided same species
            if i.same_species(j):
                #pos reward
                i.update_score(REWARD*(LENGTH/seq_length))
                j.update_score(REWARD*(LENGTH/seq_length))
            else:
                #neg reward
                i.update_score(PENALTY*(seq_length/LENGTH))
                j.update_score(PENALTY*(seq_length/LENGTH))


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

    #two step
    print('two step')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i)
        
        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, True)
            round_two(fireflies)
        
        runs[('twostep', rep)] = list_flies(fireflies)


    #normal
    print('normal')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i) 

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, True)

        runs[('normal', rep)] = list_flies(fireflies)

    '''
    #exponential
    print('exponential')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = exp_fly(i)

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, False)

        runs[('exp',rep)] = list_flies(fireflies)

    #normal
    print('normal')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i)

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, False)

        runs[('normal', rep)] = list_flies(fireflies)

    #exponential + push
    print('exponential push')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = exp_fly(i)

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, True)

        runs[('exp_push',rep)] = list_flies(fireflies)

    #normal + push
    print('normal push')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = subby_fly(i)

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch, True)

        runs[('normal_push', rep)] = list_flies(fireflies)

    '''
    print('printing')
    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
