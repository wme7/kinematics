"""Learning goals:
- Use NumPy arrays instead of Python lists for numeric work
- Compute s for all t values in one vectorized expression
- Print a table by iterating over array values with zip()
"""

import numpy as np

v0 = 2
a = 0.2
dt = 0.1  # Increment
n = int(round(2 / dt)) + 1  # No of t values

t_values = np.linspace(0, 2, n)
s_values = v0 * t_values + 0.5 * a * t_values**2

# Make nicely formatted table
for t, s in zip(t_values, s_values):
    print(f'{t:.2f}  {s:.4f}')
