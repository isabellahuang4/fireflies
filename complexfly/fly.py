# ensure periodicity in pattern with F, D, I 

import random as r
from statistics import mean
import math

LENGTH = 20

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = None
        self.simscore_list = []
        self.last_score = None #for printing purposes
        
    #sorting flies in list by species and simscore
    def __lt__(self, other):
        if self.species == other.species:
            if self.score() != None and other.score() != None:
                return self.score() < other.score()
            else:
                return self.species < other.species
        else:
            return self.species < other.species

    def __str__(self):
        return str(self.pattern) + self.recreate_pattern() + " " + str(self.species)
        
    def score(self):
        if self.simscore_list != []:
            return mean(self.simscore_list)
        else:
            return None

    #randomly generate initial pattern
    def init_pattern(self):
        #F = number of flashes
        #D = duration of one flash
        #I = interpulse interval = D + x
        # F * I < LENGTH

        #choose num_flash between 1 and length/2
        F = r.randint(1, math.floor(LENGTH/2))
        #choose duration of flash s.t. F * (D+1) < LENGTH
        D = r.randint(1, math.floor(LENGTH/F)-1)
        #choose x s.t. (D+x)*F < LENGTH
        x = r.randint(1, math.floor(LENGTH/F)-D)
        #I = D+x
        
        p = [F, D, x]
        self.pattern = p

    def recreate_pattern(self):
        p = [0] * LENGTH
        t = 0
        for i in range(self.pattern[0]):
            for j in range(self.pattern[1]):
                p[t] = 1
                t += 1
            for k in range(self.pattern[2]):
                p[t] = 0
                t += 1

        return p
            
    #return number of flashes in current pattern
    def num_flash(self):
        if self.pattern != None:
            return self.pattern[0] * self.pattern[1]
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
        X = self.recreate_pattern() + self.recreate_pattern()[:LENGTH-1]
        Y = other.recreate_pattern() + other.recreate_pattern()[:LENGTH-1]
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
        

    #choose F, D, or x to mutate
    #+/- 1 
    def mutate(self):
        F = self.pattern[0]
        D = self.pattern[1]
        x = self.pattern[2]
        choose = []
        if (F+1)*(D+x) < LENGTH:
            choose.append(0)
        if F - 1 > 0 and (F-1)*(D+x) < LENGTH:
            choose.append(1)
        if F*(D+1+x) < LENGTH:
            choose.append(2)
        if D - 1 > 0 and F*(D-1 + x) < LENGTH:
            choose.append(3)
        if F * (D+x+1) < LENGTH:
            choose.append(4)
        if x - 1 > 0 and F*(D+x-1) < LENGTH:
            choose.append(5)
            
        if choose != []:
            m = r.choice(choose)
        else:
            print('MUTATION ERROR')
            return

        if m == 0:
            self.pattern[0] += 1
        if m == 1:
            self.pattern[0] -= 1
        if m == 2:
            self.pattern[1] += 1
        if m == 3:
            self.pattern[1] -= 1
        if m == 4:
            self.pattern[2] += 1
        if m == 5:
            self.pattern[2] -= 1

        
    
