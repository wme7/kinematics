"""Learning goals:
- Use a while loop with a floating-point counter
- Update t and print (t, s) at each step
- Notice floating-point drift when repeatedly adding dt
"""

v0 = 2
a = 0.2
dt = 0.1  # Increment
t = 0     # Start value
while t <= 2:
    s = v0 * t + 0.5 * a * t**2
    print(t, s)
    t = t + dt
