import sys
import random as r
from itertools import combinations
from fly import Firefly

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 5
EPOCHS = 500
MUTATE_PROB = .1

def go(fireflies):
    for (i,j) in combinations(fireflies, 2):
        same = i.same_species(j)
        if same:
            iscore = i.num_flash()
            jscore = j.num_flash()
            if iscore < jscore:
                j.pattern = i.pattern[:]
                if r.random() < MUTATE_PROB:
                    j.mutate()
            else:
                i.pattern = j.pattern[:]
                if r.random() < MUTATE_PROB:
                    i.mutate()


def main(args):
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)
            fireflies[j+(NUM_EACH*i)].init_pattern()
            
    for epoch in range(EPOCHS):
        go(fireflies)
    for fly in fireflies:
        print(fly.pattern)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
