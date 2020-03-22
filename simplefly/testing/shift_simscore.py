#simscore looks bitbybit with shifting
#testing version

import sys
import random as r
import math
from statistics import mean

LENGTH = 6
MAX_FLASH = 4

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
        num_flash = r.randint(1, MAX_FLASH)
        indicies = r.sample(range(LENGTH), num_flash)
        for i in indicies:
            p[i] = 1
        self.pattern = p

    def same_species(self, other):
        if self.species == other.species:
            return True
        else: 
            return False

    #bit by bit similarity SHIFTED
    #smaller score is better
    def calc_similarity(self, other):
        score = 0
        #i is how much we shift
        for i in range(LENGTH):
            #j is index we're looking at rn
            for j in range(LENGTH):
                if self.pattern[(i+j)%LENGTH] == other.pattern[j]:
                    score += 1

        return score

    def reset_simscore(self):
        self.simscore = 0

    def update_simscore(self, newsim):
        if self.simscore == 0:
            self.simscore = newsim
        else:
            self.simscore = mean([self.simscore, newsim])

    #first choose whether to (0) add a flash, (1) remove a flash, or (2) move a flash
    #if already at max_flash, cannot add
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
        elif m == 2: #no limit on how far flash can move rn
            add = r.choice(current_silence)
            delete = r.choice(current_flashes)
            self.pattern[add] = 1
            self.pattern[delete] = 0

    def push_periodic(self):
        indices = []
        for i in range(LENGTH):
            if self.pattern[i] == 1:
                indices.append(i)
        differences = []
        two = False
        for i in range(len(indices)):
            if i == len(indices)-1:
                d = (indices[0] - indices[i]) % LENGTH
                if d == 1:
                    two = True
            else:
                d = (indices[i+1] - indices[i]) % LENGTH
                if d == 1:
                    two = True
            differences.append(d)

        p = [0] * LENGTH

        if two:
            zero = differences.index(1)
            i = indices[zero]
            p[i] = 1
            j = indices[(zero+1) % len(indices)]
            p[j] = 1
            a = differences[(zero+1) % len(differences)]
            p[(j+a) % LENGTH] = 1
            p[(j+a+1) % LENGTH] = 1

        else:
            avg = mean(differences)
            a = math.ceil(avg)
            b = math.floor(avg)
            i = indices[0]
            p[i] = 1
            p[(i+a)%LENGTH] = 1
            if len(indices) > 2:
                p[(i+a+b)%LENGTH] = 1
            if len(indices) > 3:
                p[(i+a+b+a)%LENGTH] = 1

        self.pattern = p
