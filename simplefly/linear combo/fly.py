# obj function as linear combo of flashing and simscore

import random as r
from statistics import mean
import math

LENGTH = 20

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.simscore_list = []
        self.last_score = None
    
    #sorting flies in list by species and simscore
    def __lt__(self, other):
        if self.species == other.species:
            if self.score() != None and other.score() != None:
                return self.score() < other.score()
            else:
                return self.species < other.species
        else:
            return self.species < other.species

    def score(self):
        if self.simscore_list != []:
            return mean(self.simscore_list)
        else:
            return None

    #randomly generate initial pattern
    def init_pattern(self):
        p = [0] * LENGTH
        num_flash = r.randint(1, LENGTH)
        indicies = r.sample(range(LENGTH), num_flash)
        for i in indicies:
            p[i] = 1
        self.pattern = p

    #return number of flashes in current pattern
    def num_flash(self):
        if self.pattern != None:
            return sum(self.pattern)
        else:
            return None

    #return whether other is of the same species
    def same_species(self, other):
        if self.species == other.species:
            return True
        else: 
            return False

    #find longest common substring
    #repeat each pattern for "wrap"
    #lower score is better
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
        self.simscore_list = []
        
    def update_simscore(self, newsim):
        self.simscore_list.append(newsim)
        

    #first choose whether to (0) add a flash, (1) remove a flash, or (2) move a flash
    #if already at max_flash, cannot add (max = length)
    def mutate(self):
        if sum(self.pattern) == LENGTH:
            m = 1
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

    #rewrite pattern with longest string of 0s at the end
    def set_start(self):
        m = 0
        zlen = 0
        z = False
        m_start = None
        zstart = None
        for i in range(LENGTH*2 - 1):
            if self.pattern[i % LENGTH] == 1:
                if zlen > m:
                    m = zlen
                    m_start = zstart
                z = False
                zlen = 0
                zstart = None
            elif z: #in the middle of zero chain
                zlen += 1
            else: #start of a zero chain
                zlen = 1
                z = True
                zstart = i

        if z and zlen > m:
            m = zlen
            m_start = zstart
            
        #print('length: ', m)
        #print('start: ', m_start)
        if m_start == None:
            p = self.pattern
        else:
            p = [self.pattern[(i+m_start+m) % LENGTH] for i in range(LENGTH)]
        
        return p
