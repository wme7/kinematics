"""
Simulate vertical vibrations of a vehicle driving on a bumpy road.

Road height profiles are read from a CSV file with columns:
x, h0, h1, ...  (distance along the road, then one or more height profiles).
"""

import os
import sys
import pickle
import urllib.request

import numpy as np


def load_road_csv(filename):
    """Load road data from CSV. Returns x (1d) and h_data (nroads, npoints)."""
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(
            f'Expected CSV with columns x,h0,... ; got shape {data.shape}')
    x = data[:, 0]
    h_data = data[:, 1:].T  # shape (nroads, npoints)
    return x, h_data


def bumpy_road(url=None, m=60, b=80, k=60, v=5, cy=False):
    """
    Solve model for vertical vehicle vibrations.

    =========   ==============================================
    variable    description
    =========   ==============================================
    url         either URL of file with road height data,
                or name of a local CSV file
    m           mass of system
    b           friction parameter
    k           spring parameter
    v           (constant) velocity of vehicle
    cy          Cython version of function solver
    Return      data (list) holding input and output data
                [x, t, [h, F, u], [h, F, u], ...]
    =========   ==============================================
    """
    # Download file (if url is not the name of a local file)
    if url.startswith('http://') or url.startswith('https://') \
            or url.startswith('file://'):
        filename = os.path.basename(url)  # strip off path
        urllib.request.urlretrieve(url, filename)
    else:
        filename = url
        if not os.path.isfile(filename):
            print(url, 'must be a URL or a filename')
            sys.exit(1)

    try:
        x, h_data = load_road_csv(filename)
    except ValueError as exc:
        print('Wrong format in file', url, ':', exc)
        sys.exit(1)

    t = x / v  # time corresponding to x
    dt = t[1] - t[0]
    if dt > 2 / np.sqrt(k / float(m)):
        print('Unstable scheme')

    if cy:
        from solver_cy import solver, Spring
        s = Spring(k)
    else:
        from solver import solver

        def s(u):
            return k * u

    data = [x, t]  # key input and output data (arrays)
    for i in range(h_data.shape[0]):
        h = h_data[i, :]
        a = acceleration(h, x, v)
        F = -m * a

        u, t = solver(I=0, V=0, m=m, b=b, s=s, F=F, t=t,
                      damping='linear')
        data.append([h, F, u])
    return data


def acceleration(h, x, v):
    """Compute 2nd-order derivative of h."""
    # Method: standard finite difference approximation
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    for i in range(1, h.size - 1, 1):
        d2h[i] = (h[i - 1] - 2 * h[i] + h[i + 1]) / dx**2
    # Extrapolate end values from first interior value
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    a = d2h * v**2
    return a


def acceleration_vectorized(h, x, v):
    """Compute 2nd-order derivative of h. Vectorized version."""
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    d2h[1:-1] = (h[:-2] - 2 * h[1:-1] + h[2:]) / dx**2
    # Extrapolate end values from first interior value
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    a = d2h * v**2
    return a


def rms(data):
    """Append root-mean-square displacement for each road realization."""
    u_rms = [np.sqrt((1.0 / len(u)) * np.sum(u**2))
             for h, F, u in data[2:]]
    data.append(u_rms)
    return data


def command_line_options():
    import argparse
    parser = argparse.ArgumentParser(
        description='Bumpy-road vehicle vibration demo')
    parser.add_argument('--m', '--mass', type=float,
                        default=60, help='mass of vehicle')
    parser.add_argument('--k', '--spring', type=float,
                        default=60, help='spring parameter')
    parser.add_argument('--b', '--damping', type=float,
                        default=80, help='damping parameter')
    parser.add_argument('--v', '--velocity', type=float,
                        default=5, help='velocity of vehicle')
    parser.add_argument('--cython', action='store_true')
    parser.add_argument('--roadfile', type=str,
                        default='bumpy.csv',
                        help='local CSV (or URL) with road data')
    args = parser.parse_args()
    return args.roadfile, args.m, args.b, args.k, args.v, args.cython


if __name__ == '__main__':
    url, m, b, k, v, cy = command_line_options()

    data = bumpy_road(url=url, m=m, b=b, k=k, v=v, cy=cy)

    # Root mean square values
    u_rms = [np.sqrt((1.0 / len(u)) * np.sum(u**2))
             for h, F, u in data[2:]]
    print('u_rms:', u_rms)
    print(f'Simulated for t in [0, {data[1][-1]:g}]')

    # Save data list to file
    with open('bumpy.res', 'wb') as outfile:
        pickle.dump(data, outfile)
