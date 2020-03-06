# naming game with TWO rounds
#first round: original game (teaching patterns and renaming based on scores)
#           : if meet opposite, do nothing
#second round: send partial pattern, make decision --> get score
#using the limitflashes fly
#using all pairings per round
#pos reward bigger for smaller subsequence
#neg penalty bigger for longer subsequence

import sys
import random as r
from itertools import combinations

LENGTH = 10
MAX_FLASH = 4
NUM_SPECIES = 2
NUM_EACH = 15 #NUM_EACH MUST BE EVEN
EPOCHS = 100
MUTATE_PROB = .1
DECISION_THRESHOLD = .7 
PENALTY = -10
REWARD = 10

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.score = None
    
    def __lt__(self, other):
        return self.species < other.species

    def init_pattern(self):
        p = [0] * LENGTH
        num_flash = r.randint(1, MAX_FLASH)
        indices = r.sample(range(LENGTH), num_flash)
        for i in indices:
            p[i] = 1
        self.pattern = p

    def same_species(self, other):
        if self.species == other.species:
            return True
        else: 
            return False

    #find longest shared substring with segment of sequence given
    # no wrapping of partial sequence
    def calc_similarity(self, seq):
        X = self.pattern + self.pattern[:LENGTH-1]
        Y = seq
        table = [[0 for k in range(len(seq)+1)] for l in range(2*LENGTH)]
        score = 0
        for i in range(2*LENGTH):
            for j in range(len(seq)+1):
                if (i == 0 or j == 0):
                    table[i][j] = 0
                elif (X[i-1] == Y[j-1]):
                    table[i][j] = table[i-1][j-1] + 1
                    score = max(score, table[i][j])
                else:
                    table[i][j] = 0

        #want to normalize with respect to length of seq
        return score/len(seq)

    def reset_score(self):
        self.score = None

    def update_score(self, new):
        if self.score == None:
            self.score = new
        else:
            self.score += new #add because it's a reward/penalty

    def mutate(self):
        if sum(self.pattern) == MAX_FLASH:
            m = r.randint(1,2)
        elif sum(self.pattern) == 1:
            m = r.choice([0,2])
        else:
            m = r.randint(0,2)
        current_flashes = []
        current_silence = []
        for i in range(LENGTH):
            if self.pattern[i] == 1:
                current_flashes.append(i)
            else:
                current_silence.append(i)
        
        if m == 0:
            add = r.choice(current_silence)
            self.pattern[add] = 1
        elif m == 1:
            delete = r.choice(current_flashes)
            self.pattern[delete] = 0
        elif m == 2:
            add = r.choice(current_silence)
            delete = r.choice(current_flashes)
            self.pattern[add] = 1
            self.pattern[delete] = 0
            
def printall(flies):
    flies.sort()
    for f in flies:
        print(f.pattern, f.species)
    print(flies[0].calc_similarity(flies[NUM_SPECIES*NUM_EACH - 1].pattern))

#returns list of pairs of flies of same species
def get_same_species(flies):
    flies.sort()
    pairs = []
    for i in range(NUM_SPECIES):
        set = flies[i*NUM_EACH: (i*NUM_EACH)+NUM_EACH]
        pairs += [(i,j) for (i,j) in combinations(set, 2)]
    return pairs

#need to check that pointers work out
def round_one(flies):
    for (i,j) in get_same_species(flies):
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
        #both have pattern
        #have gone through round 2 -- NEED TO CHECK THIS LOGIC. 
        elif i.score != None and j.score != None:
            if i.score >= j.score:
                j.pattern = i.pattern
                if r.random() < MUTATE_PROB:
                    j.mutate()
                j.reset_score()
            else:
                i.pattern = j.pattern
                if r.random() < MUTATE_PROB:
                    i.mutate()
                i.reset_score()

def round_two(flies):
    r.shuffle(flies)
    for (i,j) in combinations(flies,2):
        #i sends partial sequence
        start = r.randint(0, LENGTH-5) #note we're picking indices
        end = r.randint(start+4, LENGTH-1) #ensure that seq is at least 4 long
        seq_length = end-start
        seq = i.pattern[start:end]
        #j makes decision based on substring match with j's full pattern
        decision = j.calc_similarity(seq)
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
                

def main(args):
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)

    for epoch in range(EPOCHS):
        round_one(fireflies)
        round_two(fireflies)


    printall(fireflies)
                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
