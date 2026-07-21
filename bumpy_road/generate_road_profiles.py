"""
Generate the geometry of a bumpy road.

Method: excite an oscillator with white noise and use the
relatively smooth displacement as the height of the road.
"""

import numpy as np
from solver import solver


def generate_bumpy_road(nbumps=12, L=200, resolution=500):
    """Generate one road profile by using a vibration ODE."""
    n = nbumps * resolution       # no of compute intervals along the road
    x = np.linspace(0, L, n + 1)  # points along the road
    dx = x[1] - x[0]              # step along the road
    white_noise = np.random.randn(n + 1) / np.sqrt(dx)

    k = 1.0
    m = 4.0
    if dx > 2 / np.sqrt(k / m):
        print('Unstable scheme')

    def s(u):
        return k * u

    h, x = solver(I=0, V=0, m=m, b=3, s=s, F=white_noise,
                  t=x, damping='linear')
    h = h / h.max() * 0.2
    return h, x


def generate_bumpy_roads(L, nroads, resolution, filename='bumpy.csv'):
    """Generate many road profiles and save them as CSV (columns x, h0, h1, ...)."""
    np.random.seed(1)
    nbumps = int(L / 30.0)
    profiles = []
    x = None
    for _ in range(nroads):
        h, x = generate_bumpy_road(nbumps, L, resolution)
        profiles.append(h)

    # Column format: x, h0, h1, ...
    header = 'x,' + ','.join(f'h{i}' for i in range(nroads))
    data = np.column_stack([x] + profiles)
    np.savetxt(filename, data, delimiter=',', header=header, comments='')
    print(f'Wrote {filename} with shape {data.shape}')
    return filename


if __name__ == '__main__':
    generate_bumpy_roads(L=2000, nroads=3, resolution=500)
