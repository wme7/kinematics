import numpy as np

def load_road_csv(filename):
    """Load CSV with columns x, h0, h1, ..."""
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(
            f'Expected CSV with columns x,h0,... ; got {data.shape}')
    x = data[:, 0]
    h_data = data[:, 1:].T   # shape (nroads, npoints)
    return x, h_data
