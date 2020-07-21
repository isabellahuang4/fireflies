import csv
from statistics import variance
from statistics import mean

#convert string patterns to int patterns
def read_pattern(line):
    p = []
    for i in range(len(line)):
        if line[i] == ']':
            return p
        elif line[i] == '0' or line[i] == '1':
            p.append(int(line[i]))

#given one pattern, find variance of quiet time
#as a proxy of how periodic
def variance_quiet(pattern):
    quiet = False
    l = 0
    lengths = []
    for i in range(len(pattern)):
        if pattern[i] == 0:
            if quiet == False:
                quiet = True
                l = 1
            else:
                l += 1
        else:
            if quiet == True:
                quiet = False
                lengths.append(l)
    #if quiet == True: #for the last quiet period
        #lengths.append(l)
    if len(lengths) > 1:
        return variance(lengths)
    else:
        return 0
            
def variance_flash(pattern):
    flash = False
    l = 0
    lengths = []
    for i in range(len(pattern)):
        if pattern[i] == 1:
            if not flash:
                flash = True
                l = 1
            else:
                l += 1
        else:
            if flash:
                flash = False
                lengths.append(l)
    if flash:
        lengths.append(l)
    if len(lengths) > 1:
        return variance(lengths)
    else:
        return 0

#given list of patterns, find average of variance of quiet times
def avg_quiet(patterns):
    times = []
    for p in patterns:
        times.append(variance_quiet(p))
    return mean(times)
    

def read_in(file_path, numsp):
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            p_list = []
            for pattern in row[1:numsp+1]:
                p_list.append(read_pattern(pattern))
            print(avg_quiet(p_list))
