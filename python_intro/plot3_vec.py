"""Learning goals:
- Same physics as plot3.py, but evaluate s(t) without a Python loop
- Use np.where (or boolean indexing) for piecewise array formulas
- See why vectorization matters: same result, far fewer Python iterations
"""

import numpy as np
import matplotlib.pyplot as plt


def s_func(t, v0, a0, t1):
    """Piecewise motion for a scalar t or a NumPy array of times."""
    if isinstance(t, (float, int)):
        if t <= t1:
            s = v0 * t + 0.5 * a0 * t**2
        else:
            s = v0 * t + 0.5 * a0 * t1**2 + a0 * t1 * (t - t1)
    elif isinstance(t, np.ndarray):
        # Vectorized: one array expression instead of looping in Python
        s = np.where(t <= t1,
                     v0 * t + 0.5 * a0 * t**2,
                     v0 * t + 0.5 * a0 * t1**2 + a0 * t1 * (t - t1))
        # Alternative with boolean indexing:
        # s = np.zeros_like(t)
        # s[t <= t1] = (v0 * t + 0.5 * a0 * t**2)[t <= t1]
        # s[t > t1] = (v0 * t + 0.5 * a0 * t1**2 + a0 * t1 * (t - t1))[t > t1]
    return s


def main():
    n = 201  # No of t values for plotting
    t1 = 1.5
    v0 = 0.2
    a0 = 20

    t = np.linspace(0, 2, n + 1)
    # No Python for-loop over samples: NumPy applies the formula to all t at once
    s = s_func(t, v0=v0, a0=a0, t1=t1)

    plt.plot(t, s, 'b-')
    plt.plot([t1, t1], [0, s_func(t=t1, v0=v0, a0=a0, t1=t1)], 'r--')
    plt.xlabel('t [s]')
    plt.ylabel('s [m]')
    plt.savefig('myplot.png')
    plt.show()


if __name__ == '__main__':
    main()
