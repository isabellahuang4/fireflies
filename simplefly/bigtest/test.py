#testing everything

import sys
import random as r
import math
import csv 
from itertools import combinations
from statistics import mean

#from commonsub import Firefly as subby_fly
from shift import Firefly as shifty_fly

LENGTH = 10
NUM_SPECIES = 5
NUM_EACH = 15
EPOCHS = 1000
MUTATE_PROB = .1
DECISION_THRESHOLD = .7
PENALTY = -20
REWARD = 10 
TRIALS = 20

#given list of fireflies, the epoch number
def round_one(fireflies, epoch):
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
                mod_i = i.num_flash()/3
                mod_j = j.num_flash()/3
                if i.simscore*mod_i <= j.simscore*mod_j:
                    j.pattern = i.pattern
                    if r.random() < MUTATE_PROB and epoch < 975:
                        if r.random() < .25:
                            j.push_periodic()
                        else:
                            j.mutate()
                    j.reset_simscore()
                else:
                    i.pattern = j.pattern
                    if r.random() < MUTATE_PROB and epoch < 975:
                        if r.random() < .25:
                            i.push_periodic()
                        else:
                            i.mutate()
                    i.reset_simscore()

        else:
            if i.pattern == None:
                i.init_pattern()
            if j.pattern == None:
                j.init_pattern()
            distance = i.calc_similarity(j)
            i.update_simscore(distance)
            j.update_simscore(distance)

#for two step game, want HIGHER reward
def round_one_twostep(fireflies, epoch):
    for (i, j) in combinations(fireflies, 2):
        if i.same_species(j):
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
            #compare aggregate rewards, replicate larger
            #when replicating, do so with chance of mutation
                mod_i = i.num_flash()
                mod_j = j.num_flash()
                if i.simscore/mod_i >= j.simscore/mod_j:
                    j.pattern = i.pattern
                    if r.random() < MUTATE_PROB and epoch < 975:
                        if r.random() < .25:
                            j.push_periodic()
                        else:
                            j.mutate()
                    j.reset_simscore()
                else:
                    i.pattern = j.pattern
                    if r.random() < MUTATE_PROB and epoch < 975:
                        if r.random() < .25:
                            i.push_periodic()
                        else:
                            i.mutate()
                    i.reset_simscore()
            
def round_two(fireflies):
    r.shuffle(fireflies)
    for (i, j) in combinations(fireflies, 2):
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
        if (str(f.set_start()), f.species) not in seen:
            seen[(str(f.set_start()), f.species)] = 1
        else:
            seen[(str(f.set_start()), f.species)] += 1
            
    len1 = flies[0].num_flash()
    len2 = flies[15].num_flash()
    len3 = flies[31].num_flash()
    len4 = flies[46].num_flash()
    len5 = flies[61].num_flash()

    a = max(len1, len2)
    b = max(len1, len3)
    c = max(len2, len3)
    d = max(len1, len4)
    e = max(len2, len4)
    f = max(len3, len4)
    g = max(len1, len5)
    h = max(len2, len5)
    i = max(len3, len5)
    j = max(len4, len5)

    score1 = flies[0].calc_similarity(flies[15]) 
    score2 = flies[0].calc_similarity(flies[31]) 
    score3 = flies[15].calc_similarity(flies[31])
    score4 = flies[0].calc_similarity(flies[46])
    score5 = flies[15].calc_similarity(flies[46])
    score6 = flies[31].calc_similarity(flies[46])
    score7 = flies[0].calc_similarity(flies[61])
    score8 = flies[15].calc_similarity(flies[61])                                    
    score9 = flies[31].calc_similarity(flies[61])
    score10 = flies[46].calc_similarity(flies[61])
    score_discount = mean([score1*a, score2*b, score3*c, score4*d, score5*e, score6*f, \
                           score7*g, score8*h, score9*i, score10*j])
    score = mean([score1, score2, score3, score4, score5, score6, \
                  score7, score8, score9, score10])
    seen[score_discount] = 1
    seen[score] = 1

    return seen

def print_csv(results):
    with open('results_shift.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        
        for run in results.keys():
            row = [run]
            flies = results[run]
            row += flies

            writer.writerow(row)


def main(args):
    runs = {}

    #longest common substring
    print('longest common substring, og')
    for rep in range(TRIALS):
        print(rep)
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)
        
        for epoch in range(EPOCHS):
            round_one(fireflies, epoch)
        
        runs[('commonsub_og', rep)] = list_flies(fireflies)

    #longest common substring, two step game
    print('longest common substring, two step')
    for rep in range(TRIALS):
        print(rep)
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)

        for epoch in range(EPOCHS):
            round_one_twostep(fireflies, epoch)
            round_two(fireflies)

        runs[('commonsub_two', rep)] = list_flies(fireflies)

    '''
    #shifting                                      
    print('shifter, og')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)

        for epoch in range(EPOCHS):
            round_one(fireflies, epoch)

        runs[('shift_og', rep)] = list_flies(fireflies)
        
    #shifting, two step game
    print('shifter, two step')
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = shifty_fly(i)

        for epoch in range(EPOCHS):
            round_one_twostep(fireflies, epoch)
            round_two(fireflies)

        runs[('shift_two', rep)] = list_flies(fireflies)
    '''
         
    print('printing')
    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
