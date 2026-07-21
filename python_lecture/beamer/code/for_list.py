"""Learning goals:
- Prefer for i in range(n) over while when the count is known
- Build parallel lists, then iterate with zip()
- Compare zip-based and index-based table printing
"""

v0 = 2
a = 0.2
dt = 0.1  # Increment
t_values = []
s_values = []
n = int(round(2 / dt)) + 1  # No of t values
for i in range(n):
    t = i * dt
    s = v0 * t + 0.5 * a * t**2
    t_values.append(t)
    s_values.append(s)
print(s_values)  # Just take a look at a created list

# Make nicely formatted table
for t, s in zip(t_values, s_values):
    print(f'{t:.2f}  {s:.4f}')

# Alternative implementation
for i in range(len(t_values)):
    print(f'{t_values[i]:.2f}  {s_values[i]:.4f}')
