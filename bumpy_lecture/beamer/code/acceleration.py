import numpy as np

def acceleration(h, x, v):
    """Compute a = v**2 * h''(x) by centered differences."""
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    for i in range(1, h.size - 1):
        d2h[i] = (h[i-1] - 2*h[i] + h[i+1]) / dx**2
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    return d2h * v**2

def acceleration_vectorized(h, x, v):
    d2h = np.zeros(h.size)
    dx = x[1] - x[0]
    d2h[1:-1] = (h[:-2] - 2*h[1:-1] + h[2:]) / dx**2
    d2h[0] = d2h[1]
    d2h[-1] = d2h[-2]
    return d2h * v**2
