"""Test of bumpy.py for very long time integration."""

import os
import time
import pickle

from bumpy import bumpy_road, rms
from generate_road_profiles import generate_bumpy_roads

filename = 'bumpy.csv'
if not os.path.isfile(filename):
    t0 = time.perf_counter()
    generate_bumpy_roads(L=2000, nroads=3, resolution=3000,
                         filename=filename)
    t1 = time.perf_counter()
    print('Generate data:', t1 - t0)
else:
    t1 = time.perf_counter()

for cy in [False]:
    data = bumpy_road(url=filename, cy=cy)
    t2 = time.perf_counter()
    data = rms(data)
    t3 = time.perf_counter()
    with open('bumpy.res', 'wb') as outfile:
        pickle.dump(data, outfile)
    t4 = time.perf_counter()

    print('Cython acceleration:', cy)
    print('Solve equation:', t2 - t1)
    print('Compute rms:', t3 - t2)
    print('Pickle to file:', t4 - t3)
