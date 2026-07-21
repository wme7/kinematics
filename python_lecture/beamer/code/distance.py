"""Learning goals:
- Evaluate a simple kinematic expression: s = v0*t + 0.5*a*t**2
- Print numbers with default and formatted output (f-strings)
"""

t = 0.5
v0 = 2
a = 0.2
s = v0 * t + 0.5 * a * t**2
print(s)
print(f's={s:g}')
print(f's\t = \t {s:.3f}')
