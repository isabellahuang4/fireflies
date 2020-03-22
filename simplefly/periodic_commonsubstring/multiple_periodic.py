# multiple sim scores for simulation with multiple species

import sys
import random as r
from statistics import mean

LENGTH = 10
NUM_SPECIES = 3
NUM_EACH = 20
EPOCHS = 2000
PERTURB_PROB = .3
MUTATE_PROB = .1 

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.simscore = [0] * NUM_SPECIES
    
    def __lt__(self, other):
        #NEED TO HAVE AVG OF ALL OTHER ONES
        if self.species == other.species:
            me_a = sum(self.simscore) / 2
            other_a = sum(other.simscore) / 2
            return me_a < other_a 
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
        self.simscore = [0] * NUM_SPECIES

    def update_simscore(self, newsim, other_species):
        if self.simscore[other_species] == 0:
            self.simscore[other_species] = newsim
        else:
            self.simscore[other_species] = mean([self.simscore[other_species], newsim])

    def mutate(self):
        for i in range(LENGTH):
            if r.random() < PERTURB_PROB:
                self.pattern[i] = (self.pattern[i] + 1) %2

def printall(flies):
    flies.sort()
    for f in flies:
        print(f.pattern, f.species)
    print(flies[0].calc_similarity(flies[NUM_EACH + 1]))
    print(flies[0].calc_similarity(flies[NUM_EACH*2+1]))
    print(flies[NUM_EACH+1].calc_similarity(flies[NUM_EACH*2 +1]))
    
def other_species(my_species):
    a = []
    for i in range(NUM_SPECIES):
        if i != my_species:
            a += [i]
    return a


def main(args):
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)

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
                    #randomly choose species to respectively compare sim scores
                    #replicate pattern of smaller simscore
                    #when replicating, do so with chance of mutation
                    focus = r.choice(other_species(fireflies[i].species))
                    
                    if fireflies[i].simscore[focus] <= fireflies[j].simscore[focus]:
                        fireflies[j].pattern = fireflies[i].pattern
                        if r.random() < MUTATE_PROB and epoch < 1975:
                            fireflies[j].mutate()
                        fireflies[j].reset_simscore()
                    else:
                        fireflies[i].pattern = fireflies[j].pattern
                        if r.random() < MUTATE_PROB and epoch < 1975:
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


    printall(fireflies)
                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))