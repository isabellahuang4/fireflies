import sys
import csv
import pickle

def read_pattern(line):
    p = []
    for i in range(len(line)):
        if line[i] == ']':
            return str(p)
        elif line[i] == '0' or line[i] == '1':
            p.append(int(line[i]))

def main(args):
    FILE_PATH = args[0]
    num_sp = int(args[1])
    new = []
    with open('distances.pickle', 'rb') as d:
        distances = pickle.load(d)
    with open(FILE_PATH) as f:
        reader = csv.reader(f)
        for row in reader:
            new_r = []
            new_r.append(row[0])
            for pattern in row[1:num_sp+1]:
                p = read_pattern(pattern)
                new_r.append(p)
                dis = distances[p]
                new_r.append(dis)
            new.append(new_r)

    with open('distances-'+args[1]+'.csv', 'w') as file:
        writer = csv.writer(file)
        for row in new:
            writer.writerow(row)

            

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
                
    
