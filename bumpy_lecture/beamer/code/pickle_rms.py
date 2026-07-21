import pickle
import numpy as np

# After bumpy_road(...):
u_rms = [np.sqrt((1.0/len(u))*np.sum(u**2))
         for h, F, u in data[2:]]
print('u_rms:', u_rms)

with open('bumpy.res', 'wb') as outfile:
    pickle.dump(data, outfile)
