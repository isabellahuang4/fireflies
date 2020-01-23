#learning pattern and distinctiveness thru random interactions
#choose one interaction per firefly each epoch
#can consider this fully connected but with randomness???
#THIS CONVERGES
import sys
import random as r
from statistics import mean

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 20
EPOCHS = 100
PERTURB_PROB = .3
MUTATE_PROB = .1 #can we have mutate_prob change as inverse fxn of #epochs? 
#not too realistic, but helps convergence... (explore v exploit)

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.simscore = 0
    
    def __lt__(self, other):
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

    #can we find a sim function that de-emphasizes sim in 0s? 
    # more realistic?
    # higher is more similar w.r.t 1s
    def calc_similarity2(self, other):
        ct = 0
        for i in range(LENGTH):
            if self.pattern[i] != other.pattern[i] and self.pattern[i] != 0:
                ct += 1
        return ct
    
    # 0 is same, LENGTH is completely different
    def calc_similarity(self, other):
        ct = 0
        for i in range(LENGTH):
            if self.pattern[i] != other.pattern[i]:
                ct += 1
        return ct

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
                    #compare aggregate sim scores, replicate higher one 
                    #with probability simscore/length
                    #when replicating, do so with chance of mutation
                    if fireflies[i].simscore >= fireflies[j].simscore:
                        if r.random() < (fireflies[i].simscore/LENGTH):
                            fireflies[j].pattern = fireflies[i].pattern
                            if r.random() < MUTATE_PROB and epoch < 75:
                                fireflies[j].mutate()
                            fireflies[j].reset_simscore()
                    else:
                        if r.random() < (fireflies[j].simscore/LENGTH):
                            fireflies[i].pattern = fireflies[j].pattern
                            if r.random() < MUTATE_PROB and epoch < 75:
                                fireflies[i].mutate()
                            fireflies[i].reset_simscore()
            #diff species
            else:
                if fireflies[i].pattern == None:
                    fireflies[i].init_pattern()
                if fireflies[j].pattern == None:
                    fireflies[j].init_pattern()
                distance = fireflies[i].calc_similarity2(fireflies[j])
                fireflies[i].update_simscore(distance)
                fireflies[j].update_simscore(distance)


    printall(fireflies)
                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
