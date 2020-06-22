import sys
import pickle
import math
import itertools

LENGTH = 20

def distance(p1, p2):
    a = []
    b = []
    for i in range(len(p1)):
        if p1[i] == '1' or p1[i] == '0':
            a.append(p1[i])
    for i in range(len(p2)):
        if p2[i] == '1' or p2[i] == '0':
            b.append(p2[i])
    table = [[0 for x in range(LENGTH + 1)] for x in range(LENGTH + 1)]
    for i in range(LENGTH +1):
        for j in range(LENGTH + 1):
            if i == 0:
                table[i][j] = j
            elif j == 0:
                table[i][j] = i
            elif a[i-1] == b[j-1]:
                table[i][j] = table[i-1][j-1]
            else:
                table[i][j] = 1 + min(table[i][j-1], \
                                      table[i-1][j],)# \
                                      #table[i-1][j-1])
    return table[LENGTH][LENGTH]
             
def pattern(f, d, x):
    p = [0] * LENGTH
    t = 0
    for i in range(f):
        for j in range(d):
            p[t] = 1
            t += 1
        for k in range(x):
            p[t] = 0
            t += 1
    return str(p)

def set_start(p):
    m = 0
    zlen = 0
    z = False
    m_start = None
    zstart = None
    for i in range(LENGTH*2 - 1):
        if p[i % LENGTH] == 1:
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

    if m_start != None:
        p = [p[(i+m_start+m) % LENGTH] for i in range(LENGTH)]

    return p

def main(args):
    #create all possible periodic patterns
    #store dict of all periodic patterns
    '''
    periodic = {}

    for f in range(1, int(math.ceil(LENGTH/2.0))):
        for d in range(1, LENGTH/f):
            for x in range(1, (LENGTH/f) - d + 1):
                p = pattern(f,d,x)
                if p in periodic:
                    periodic[p] += 1
                else:
                    periodic[p] = 1
    
    with open('periodic.pickle', 'wb') as file:
        pickle.dump(periodic, file, protocol=pickle.HIGHEST_PROTOCOL)

    '''
    with open('periodic.pickle', 'rb') as file:
        periodic = pickle.load(file)
    
    '''
    #create all possible patterns and REWRITE
    all_p = {}
    for item in itertools.product([0,1], repeat = LENGTH):
        p = set_start(list(item))
        if str(p) not in all_p:
            all_p[str(p)] = 1
    
    
    with open('all.pickle', 'wb') as file:
        pickle.dump(all_p, file, protocol = pickle.HIGHEST_PROTOCOL)

    '''
    with open('all.pickle', 'rb') as file:
        all_patterns = pickle.load(file)

    #for nonperiodic, find closest pariodic -- store edit distance
    distances = {}
    for p in all_patterns:
        if p not in periodic:
            min = LENGTH*2
            for purp in periodic:
                dist = distance(p, purp)
                if dist < min:
                    min = dist
            distances[p] = min
        else:
            distances[p] = 0

    with open('distances_noswap.pickle', 'wb') as file:
        pickle.dump(distances, file, protocol = pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
