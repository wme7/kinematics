"""Plot road height profiles from bumpy.csv."""

import numpy as np
import matplotlib.pyplot as plt


def main():
    data = np.loadtxt('bumpy.csv', delimiter=',', skiprows=1)
    x = data[:, 0]
    h = data[:, 1:].T  # shape (nroads, npoints)

    # Show only a short segment so the bumps are visible
    m = max(len(x) // 40, 2)
    for i in range(h.shape[0]):
        plt.plot(x[:m], h[i, :m], label=f'Road {i}')

    plt.xlabel('x [m]')
    plt.ylabel('h [m]')
    plt.title('Bumpy road profiles (first segment)')
    plt.legend()
    plt.savefig('road_profiles.png')
    plt.show()


if __name__ == '__main__':
    main()
