import numpy as np
import sympy as sp
from solver import solver

def lhs_eq(t, m, b, s, u, damping='linear'):
    v = sp.diff(u, t)
    d = b*v if damping == 'linear' else b*v*sp.Abs(v)
    return m*sp.diff(u, t, t) + d + s(u)

def test_solver():
    I, V, m, b, k = 1.2, 3.0, 2.0, 0.9, 4.0
    s = lambda u: k*u
    t = sp.Symbol('t')
    time = np.linspace(0, 2.0, 11)
    u_exact = I + V*t + 2*t**2
    F = sp.lambdify(t, lhs_eq(t, m, b, s, u_exact), 'numpy')
    u, t_ = solver(I, V, m, b, s, F, time, 'linear')
    assert abs(sp.lambdify(t, u_exact, 'numpy')(t_) - u).max() < 1e-13
