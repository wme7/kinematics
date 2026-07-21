"""Learning goals:
- Plot s(t) with Matplotlib
- Label axes with physical units
- Save a figure and show it only when run as a script
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    v0 = 0.2
    a = 2
    n = 21  # No of t values for plotting

    t = np.linspace(0, 2, n + 1)
    s = v0 * t + 0.5 * a * t**2

    plt.plot(t, s)
    plt.xlabel('t [s]')
    plt.ylabel('s [m]')
    plt.savefig('myplot.png')
    plt.show()


if __name__ == '__main__':
    main()
