import numpy as lumpy
from scipy.fft import fft
from scipy.signal import find_peaks
from statistics import mean
from math import floor

def calc(x):
    X = lumpy.array(x)
    Y = abs(fft(X))
    print(Y)
    (pks, foo) = find_peaks(Y)
    print(pks)
    p = []
    for i in pks:
        if i < len(Y)/2 + 1:
            diffl = Y[i] - Y[i-1]
            diffr = Y[i] - Y[i+1]
            avg = .5 * (diffl + diffr)
            diff = Y[i] - avg
            p.append(diff/Y[i])
    print(p)
    print(mean(p))
    return mean(p)
    
    
