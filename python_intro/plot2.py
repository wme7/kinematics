"""Learning goals:
- Compare two curves on the same axes
- Use line styles, labels with units, and a legend
- Keep legend text in sync with the plotted parameters
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    v0 = 0.2
    a0 = 2
    a1 = 3
    n = 21  # No of t values for plotting

    t = np.linspace(0, 2, n + 1)
    s0 = v0 * t + 0.5 * a0 * t**2
    s1 = v0 * t + 0.5 * a1 * t**2

    plt.plot(t, s0, 'r-',  # Plot s0 curve with red line
             t, s1, 'bo')  # Plot s1 curve with blue circles
    plt.xlabel('t [s]')
    plt.ylabel('s [m]')
    plt.title('Distance plot')
    plt.legend([rf'$s(t; v_0={v0}, a={a0})$',
                rf'$s(t; v_0={v0}, a={a1})$'],
               loc='upper left')
    plt.savefig('myplot.png')
    plt.show()


if __name__ == '__main__':
    main()
