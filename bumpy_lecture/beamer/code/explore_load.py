import pickle
from numpy import *
from matplotlib.pyplot import *

with open('bumpy.res', 'rb') as outfile:
    data = pickle.load(outfile)

x, t = data[0:2]
t_s = 180
indices = t >= t_s
t = t[indices]
x = x[indices]
