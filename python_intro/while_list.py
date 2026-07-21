"""Learning goals:
- Collect results in lists with append()
- Print a formatted table after the loop finishes
- Use i += 1 as compact form of i = i + 1
"""

v0 = 2
a = 0.2
dt = 0.1  # Increment
t = 0
t_values = []
s_values = []
while t <= 2.1:
    s = v0 * t + 0.5 * a * t**2
    t_values.append(t)
    s_values.append(s)
    t = t + dt
print(s_values)  # Just take a look at a created list
print(t_values)

# Print a nicely formatted table
i = 0
while i <= len(t_values) - 1:
    print(f'{t_values[i]:.18f}  {s_values[i]:.4f}')
    i += 1  # Compact form for i = i + 1
