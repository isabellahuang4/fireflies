#naming game

import sys
import random as r
import math
import csv 
from itertools import combinations
from statistics import mean
from timeit import default_timer as timer

from fly import Firefly

LENGTH = 20
NUM_SPECIES = 7
NUM_EACH = 10
EPOCHS = 500
MUTATE_PROB = .1
TRIALS = 10

#given list of fireflies, the epoch number
#implement original naming game 
def round_one(fireflies, epoch, A, B):
    for (i, j) in combinations(fireflies, 2):
        same = i.same_species(j)
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
            elif i.score() != None and j.score() != None:
            #compare lincombo, replicate smaller one
                iscore = (A*i.score()) + (B*i.num_flash())
                jscore = (A*j.score()) + (B*j.num_flash())
                if iscore <= jscore:
                    j.pattern = i.pattern[:]
                    if r.random() < MUTATE_PROB and epoch < 495:
                        j.mutate()
                    j.reset_simscore()
                    j.last_score = iscore
                else:
                    i.pattern = j.pattern[:]
                    if r.random() < MUTATE_PROB and epoch < 495:
                        i.mutate()
                    i.reset_simscore()
                    i.last_score = jscore

        else:
            #calculate and update similarity score
            if i.pattern == None:
                i.init_pattern()
            if j.pattern == None:
                j.init_pattern()
            distance = i.calc_similarity(j)
            i.update_simscore(distance)
            j.update_simscore(distance)

#printing results
def list_flies(flies):
    flies.sort()
    seen = {}
    for f in flies:
        if (str(f.set_start()), f.species) not in seen:
            seen[(str(f.set_start()), f.species)] = f.last_score
        elif f.last_score < seen[(str(f.set_start()), f.species)]:
            seen[(str(f.set_start()), f.species)] = f.last_score
            
    return seen

#write to csv
def print_csv(results):
    with open('results.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        
        for run in results.keys():
            row = [run]
            flies = results[run]
            row += flies
            row += flies.values()
            writer.writerow(row)


def main(args):
    #keep track of all the results
    runs = {}

    a = [.2, .4, .6, .8, 1]
    
    for A in a:
        B = 1-A
        print(A,B)
        for rep in range(TRIALS):
            fireflies = [0] * (NUM_SPECIES * NUM_EACH)
            for i in range(NUM_SPECIES):
                for j in range(NUM_EACH):
                    fireflies[j+(NUM_EACH*i)] = Firefly(i)

            start = timer()
            for epoch in range(EPOCHS):
                r.shuffle(fireflies)
                round_one(fireflies, epoch, A, B)
            end = timer()
            
            runs[(A, B, rep)] = list_flies(fireflies)
            print(rep, end-start)

    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
