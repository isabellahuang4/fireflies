#recording twostepgame

import sys
import random as r
from statistics import mean
from twostepgame import Firefly
from twostepgame import round_one
from twostepgame import round_two
import csv

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 20
EPOCHS = 500
FIRST_ROUNDS = 2
SECOND_ROUNDS = 5
PERTURB_PROB = .3
MUTATE_PROB = .1 
DECISION_THRESHOLD = .7
PENALTY = -10
REWARD = 10
REPEATS = 25


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
    with open('results_2step.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        
        for run in results.keys():
            row = [run]
            flies = results[run]
            row += flies
            
            writer.writerow(row)


def main(args):
    runs = {}
    for rep in range(REPEATS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = Firefly(i)
        
        for epoch in range(EPOCHS):
            for round in range(FIRST_ROUNDS):
                if epoch != 0 or round != 0:
                    r.shuffle(fireflies)
                round_one(fireflies)
                if epoch == 0:
                    break

            for round in range(SECOND_ROUNDS):
                r.shuffle(fireflies)
                round_two(fireflies)

        runs[rep] = list_flies(fireflies)

    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
 
