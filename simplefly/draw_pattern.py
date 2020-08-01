import turtle as t
import matplotlib.pyplot as plot
import csv
import numpy as lumpy
from PIL import Image

#given list of patterns as list of integers, draws in turtle 
def draw(patterns):
    t.setup(1010,1010,0,0)
    t.fillcolor('#ffff00')
    t.penup()
    y = 410
#    for p in patterns:
#        p += p
    for p in patterns:
        y -= 60 
        for i in range(len(p)):
            if p[i] == 1:
                t.goto(-500+(i*25),y)
                t.pendown()
                t.begin_fill()
                t.goto(-475+(i*25),y)
                t.goto(-475+(i*25),y-50)
                t.goto(-500+(i*25),y-50)
                t.goto(-500+(i*25),y)
                t.end_fill()
                t.penup()
    t.done()


#given list of patterns as list of integers, draws in matplotlib
def draw_plot(patterns):
    fig, ax = plot.subplots()
    max_len = 0
    for j in range(len(patterns)):
        p = patterns[j]
        bars = []
        if len(p) > max_len:
            max_len = len(p)
        for i in range(len(p)):
            if p[i] == 1:
                bars.append((10*i,10))
        ax.broken_barh(bars, (5*j,4), facecolors='y')
        ax.broken_barh([(10*len(p), 1)], (5*j,4), facecolors='k')

    ax.set_ylim(0,len(patterns)*5)
    #need to decide whether the zoom to max allowable length or max seen length
    ax.set_xlim(0,max_len*10+2)
    ax.grid(True)
    plot.show()

#convert string patterns to int patterns
def read_pattern(line):
    p = []
    for i in range(len(line)):
        if line[i] == ']':
            return p
        elif line[i] == '0' or line[i] == '1':
            p.append(int(line[i]))


#read in results from csv and draw patterns
def read_in(file_path, numsp):
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            p_list = []
            for pattern in row[1:numsp+1]:
                p_list.append(read_pattern(pattern))
            draw_plot(p_list)
                
            
def plot_pics(pictures):
    fig = plot.figure()
    f, axarr = plot.subplots()
    for i in range(len(pictures)):
        p = pictures[i]
        img = fig.figimage(lumpy.array(Image.open(p)), xo= i*1280, yo = i*960, resize = True)
    plot.show()

        
