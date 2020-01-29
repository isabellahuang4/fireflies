#learning patterns thru interactions
#learning distinctions thru interactions
import sys
import random as r
from statistics import mean

LENGTH = 10
NUM_SPECIES = 2
NUM_EACH = 20
EPOCHS = 1
THRESHOLD = 1

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

    # 0 is same, LENGTH is completely different
    def calc_similarity(self, other):
        ct = 0
        for i in range(LENGTH):
            if self.pattern[i] != other.pattern[i]:
                ct += 1
        return ct

    def update_simscore(self, newsim):
        if self.simscore == 0:
            self.simscore = newsim
        else:
            self.simscore = mean([self.simscore, newsim])
    
def main(args):
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)
    r.shuffle(fireflies)

    for epoch in range(EPOCHS):
        #fully connected graph
        for i in range(NUM_SPECIES * NUM_EACH):
            for j in range(i+1, NUM_SPECIES * NUM_EACH):
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
                        if fireflies[i].simscore >= fireflies[j].simscore:
                            fireflies[j].pattern = fireflies[i].pattern
                        else:
                            fireflies[i].pattern = fireflies[j].pattern
                #diff species
                else:
                    if fireflies[i].pattern == None:
                        fireflies[i].init_pattern()
                    if fireflies[j].pattern == None:
                        fireflies[j].init_pattern()
                    distance = fireflies[i].calc_similarity(fireflies[j])
                    fireflies[i].update_simscore(distance)
                    fireflies[j].update_simscore(distance)

                
        #for f in fireflies:
        #    print(f.pattern, f.species)
    
    fireflies.sort()
    for f in fireflies:
        print(f.pattern, f.species)
                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
