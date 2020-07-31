import csv
import pickle

MAX_LEN = 140

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


def convert_pattern(line):
    num_flash = int(line[1])
    flash_len = int(float(line[2])*10)
    quiet = int(float(line[3])*10) - flash_len
    #silence = int(float(line[4])*10) - (num_flash * (flash_len+quiet))

    p = [0] * int(float(line[4])*10)
    t = 0
    for i in range(num_flash):
        for j in range(flash_len):
            p[t] = 1
            t += 1
        for k in range(quiet):
            p[t] = 0
            t += 1

    return p
            
    
def create_patterns(file_path):
    p_list = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'species':
                p_list.append(convert_pattern(row))

    with open(file_path[:-4]+'.pickle', 'wb') as file:
        pickle.dump(p_list, file, protocol = pickle.HIGHEST_PROTOCOL)

        
