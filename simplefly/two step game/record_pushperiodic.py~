#recording twostepgame with limitflash fly

import sys
import random as r
from tworound_limitflashes import Firefly
from tworound_limitflashes import round_one
from tworound_limitflashes import round_two
from draw_pattern import draw_patterns
import csv

EPOCHS = 600
TRIALS = 20
NUM_SPECIES = 3
NUM_EACH = 15


def list_flies(flies):
    flies.sort()
    seen = {}
    for f in flies:
        if (str(f.pattern), f.species) not in seen:
            seen[(str(f.pattern), f.species)] = 1
        else:
            seen[(str(f.pattern), f.species)] += 1

    #assume convergence and get simscore
    score1 = flies[0].calc_similarity(flies[29].pattern)
    seen[score1] = 1
    score2 = flies[0].calc_similarity(flies[44].pattern)
    seen[score2] = 1
    score3 = flies[29].calc_similarity(flies[44].pattern)
    seen[score3] = 1
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
    for rep in range(TRIALS):
        fireflies = [0] * (NUM_SPECIES * NUM_EACH)
        for i in range(NUM_SPECIES):
            for j in range(NUM_EACH):
                fireflies[j+(NUM_EACH*i)] = Firefly(i)
        
        for epoch in range(EPOCHS):
            round_one(fireflies)
            round_two(fireflies)

        runs[rep] = list_flies(fireflies)

    print_csv(runs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
 
