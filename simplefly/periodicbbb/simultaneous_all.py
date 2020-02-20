#all pairs interact each epoch.

import sys
import random as r
from statistics import mean
from itertools import combinations

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 10
EPOCHS = 200
PERTURB_PROB = .3
MUTATE_PROB = .1 

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.simscore = 0
    
    def __lt__(self, other):
        if self.species == other.species:
            return self.simscore < other.simscore
        else:
            return self.species < other.species

    def init_pattern(self):
        p = [0] * LENGTH
        for i in range(LENGTH):
            if r.random() < .5:
                p[i] = 1
        self.pattern = p

    def same_species(self, other):
        if self.species == other.species:
            return True
        else: 
            return False

    #find longest shared substring
    #repeat each pattern so we get the "wrap"
    #smol similarity is better
    def calc_similarity(self, other):
        X = self.pattern + self.pattern[:LENGTH-1]
        Y = other.pattern + other.pattern[:LENGTH-1]
        table = [[0 for k in range(2*LENGTH)] for l in range(2*LENGTH)]
        score = 0
        for i in range(2*LENGTH):
            for j in range(2*LENGTH):
                if (i == 0 or j == 0):
                    table[i][j] = 0
                elif (X[i-1] == Y[j-1]):
                    table[i][j] = table[i-1][j-1] + 1
                    score = max(score, table[i][j])
                else:
                    table[i][j] = 0

        return score

    def reset_simscore(self):
        self.simscore = 0

    def update_simscore(self, newsim):
        if self.simscore == 0:
            self.simscore = newsim
        else:
            self.simscore = mean([self.simscore, newsim])

    def mutate(self):
        for i in range(LENGTH):
            if r.random() < PERTURB_PROB:
                self.pattern[i] = (self.pattern[i] + 1) %2

def printall(flies):
    flies.sort()
    for f in flies:
        print(f.pattern, f.species)
    print(flies[0].calc_similarity(flies[NUM_SPECIES*NUM_EACH - 1]))
    
def main(args):
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)

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
                        if r.random() < MUTATE_PROB and epoch < 175:
                            j.mutate()
                        j.reset_simscore()
                    else:
                        i.pattern = j.pattern
                        if r.random() < MUTATE_PROB and epoch < 975:
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


    printall(fireflies)
                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
