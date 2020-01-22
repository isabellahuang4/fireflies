import sys
import random as r

LENGTH = 10
NUM_SPECIES = 2
EPOCHS = 3000
PERTURB_PROB = .2

def init_pattern():
    p = [0] * LENGTH
    for i in range(LENGTH):
        if r.random() < .5:
            p[i] = 1
    return p

def perturb(p):
    new_p = [0] * LENGTH
    for i in range(LENGTH):
        if r.random() < PERTURB_PROB:
            new_p[i] = (p[i] + 1) % 2
    return new_p

#0 if same, LENGTH if completely different
def calc_similarity(p1, p2):
    ct = 0
    for i in range(LENGTH):
        if p1[i] != p2[i]:
            ct += 1
    return ct
            

def main(args):
    #randomly generate patterns for each species
    patterns = []
    for i in range(NUM_SPECIES):
        patterns.append(init_pattern())
    
    for epoch in range(EPOCHS):
        orig_sim = calc_similarity(patterns[0], patterns[1])
        #perturb one of the patterns
        change = r.choice(range(NUM_SPECIES))
        remain = (change + 1) % 2
        new = perturb(patterns[change])
        if calc_similarity(new, patterns[remain]) > orig_sim:
            print('change', calc_similarity(new, patterns[remain]))
            patterns[change] = new        
            
    print(calc_similarity(patterns[0], patterns[1]))
    print(patterns[0])
    print(patterns[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
