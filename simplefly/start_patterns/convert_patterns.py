import csv
import pickle

def read_pattern(line):
    p = []
    for i in range(len(line)):
        if line[i] == '0' or line[i] == '1':
            p.append(int(line[i]))
    return p

def read_in(file_path):
    p_list = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            p_list.append(read_pattern(row))
    
    with open(file_path[:-4]+'.pickle', 'wb') as file:
        pickle.dump(p_list, file, protocol = pickle.HIGHEST_PROTOCOL)
