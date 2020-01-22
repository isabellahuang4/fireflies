#first pass, has fly as object
import sys
import random as r

LENGTH = 2
NUM_SPECIES = 2
NUM_EACH = 5
EPOCHS = 100
THRESHOLD = 1

class Firefly():
    def __init__(self, species):
        self.species = species #which num species
        self.pattern = self.init_pattern()
    
    def __lt__(self, other):
        return self.species < other.species

    def init_pattern(self):
        p = [0] * LENGTH
        for i in range(LENGTH):
            if r.random() < .5:
                p[i] = 1
        return p

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

    def change_pattern(self, factor):
        for i in range(LENGTH):
            if r.random() < factor/LENGTH:
                self.pattern[i] = (self.pattern[i] + 1) % 2
            
    
def main(args):
    """
    a = Firefly(1)
    b = Firefly(1)
    print(a.same_species(b))
    print(a.calc_similarity(b))
    """
    #create fireflies
    fireflies = [0] * (NUM_SPECIES * NUM_EACH)
    for i in range(NUM_SPECIES):
        for j in range(NUM_EACH):
            fireflies[j+(NUM_EACH*i)] = Firefly(i)
    r.shuffle(fireflies)

    for epoch in range(EPOCHS):
        #use fully connected graph for now
        for i in range(NUM_SPECIES * NUM_EACH):
            for j in range(i+1, NUM_SPECIES * NUM_EACH):
                same = fireflies[i].same_species(fireflies[j])
                distance = fireflies[i].calc_similarity(fireflies[j])
                if same and distance > THRESHOLD:
                    fireflies[i].change_pattern(distance)
                    fireflies[j].change_pattern(distance)
                elif not same and distance <= THRESHOLD:
                    fireflies[i].change_pattern(distance)
                    fireflies[j].change_pattern(distance)
                
        #for f in fireflies:
            #print(f.pattern, f.species)
    
    fireflies.sort()
    for f in fireflies:
        print(f.pattern, f.species)


                    



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
