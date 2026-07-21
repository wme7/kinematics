"""Learning goals:
- Define a piecewise kinematic function s(t)
- Evaluate it with an explicit Python loop over time samples
- Contrast this approach with the vectorized version in plot3_vec.py
"""

import numpy as np
import matplotlib.pyplot as plt


def s_func(t, v0, a0, t1):
    """Scalar piecewise motion: accelerate until t1, then constant velocity."""
    if t <= t1:
        s = v0 * t + 0.5 * a0 * t**2
    else:
        s = v0 * t + 0.5 * a0 * t1**2 + a0 * t1 * (t - t1)
    return s


def main():
    n = 201  # No of t values for plotting
    t1 = 1.5
    v0 = 0.2
    a0 = 20

    t = np.linspace(0, 2, n + 1)
    # Explicit Python loop: clear, but slow for large n (see plot3_vec.py)
    s = np.zeros(n + 1)
    for i in range(len(t)):
        s[i] = s_func(t=t[i], v0=v0, a0=a0, t1=t1)

    plt.plot(t, s, 'b-')
    plt.plot([t1, t1], [0, s_func(t=t1, v0=v0, a0=a0, t1=t1)], 'r--')
    plt.xlabel('t [s]')
    plt.ylabel('s [m]')
    plt.savefig('myplot.png')
    plt.show()


if __name__ == '__main__':
    main()
