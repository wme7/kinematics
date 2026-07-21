"""Learning goals:
- Read simulation parameters from a YAML file
- Write a formatted results table to a text file
- Compare manual writing with numpy.savetxt / loadtxt
"""

import numpy as np
import yaml

with open('input.yaml') as infile:
    params = yaml.safe_load(infile)

v0 = params['v0']
a = params['a']
dt = params['dt']
interval = params['interval']

t_values = []
s_values = []
n = int(round(interval[1] / dt)) + 1  # No of t values
for i in range(n):
    t = i * dt
    s = v0 * t + 0.5 * a * t**2
    t_values.append(t)
    s_values.append(s)

# Write nicely formatted table to file
with open('table1.dat', 'w') as outfile:
    outfile.write('# t    s(t)\n')  # write table header
    for t, s in zip(t_values, s_values):
        outfile.write(f'{t:.2f}  {s:.4f}\n')

# Alternative: use numpy.savetxt
# Make two-dimensional array of [t, s(t)] values in each row
data = np.array([t_values, s_values]).transpose()

# Write data array to file in table format
np.savetxt('table2.dat', data, fmt=['%.2f', '%.4f'],
           header='t   s(t)', comments='# ')

# Read the file back
data = np.loadtxt('table2.dat', comments='#')
