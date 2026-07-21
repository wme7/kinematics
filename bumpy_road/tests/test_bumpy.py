"""Tests for the bumpy-road ODE solver and road acceleration helpers."""

import numpy as np
import pytest
import sympy as sp

from bumpy import acceleration, acceleration_vectorized
from solver import solver, solver_linear_damping


def lhs_eq(t, m, b, s, u, damping='linear'):
    """Return lhs of differential equation as a sympy expression."""
    v = sp.diff(u, t)
    d = b * v if damping == 'linear' else b * v * sp.Abs(v)
    return m * sp.diff(u, t, t) + d + s(u)


def test_acceleration():
    x = np.linspace(0, 10, 5)
    h = x**2
    v = np.sqrt(0.5)
    # v**2*h'' should equal 1 exactly, except perhaps at
    # the end points where we extrapolate
    a_s = acceleration(h, x, v)
    a_v = acceleration_vectorized(h, x, v)
    diff = np.abs(a_s - a_v).max()
    assert diff == pytest.approx(0.0, abs=1e-14)


def test_solver():
    """Verify linear/quadratic manufactured solutions for solver()."""
    I = 1.2
    V = 3.0
    m = 2.0
    b = 0.9
    k = 4.0
    s = lambda u: k * u
    T = 2.0
    dt = 0.2
    N = int(round(T / dt))
    time_points = np.linspace(0, T, N + 1)
    t = sp.Symbol('t')
    tol = 1e-13

    # Linear damping: quadratic exact solution
    q = 2
    u_exact = I + V * t + q * t**2
    F_term = lhs_eq(t, m, b, s, u_exact, 'linear')
    F = sp.lambdify([t], F_term, modules='numpy')
    u, t_ = solver(I, V, m, b, s, F, time_points, 'linear')
    u_e = sp.lambdify([t], u_exact, modules='numpy')
    assert abs(u_e(t_) - u).max() < tol

    # Quadratic damping: exact solution must be linear
    u_exact = I + V * t
    F_term = lhs_eq(t, m, b, s, u_exact, 'quadratic')
    F = sp.lambdify([t], F_term, modules='numpy')
    u, t_ = solver(I, V, m, b, s, F, time_points, 'quadratic')
    u_e = sp.lambdify([t], u_exact, modules='numpy')
    assert abs(u_e(t_) - u).max() < tol


def _solver_linear_damping_wrapper(I, V, m, b, s, F, t, damping='linear'):
    """Call solver_linear_damping with the same signature as solver()."""
    if callable(F):
        F = F(t)
    return solver_linear_damping(I, V, m, b, s, F, t), t


def _available_solvers():
    functions = [solver, _solver_linear_damping_wrapper]
    try:
        from solver_cy import solver as solver_cy
        functions.append(solver_cy)
    except ImportError:
        pass
    return functions


@pytest.mark.parametrize('function', _available_solvers(),
                         ids=lambda f: f.__name__)
def test_all_functions(function):
    """Verify manufactured solutions for each available solver variant."""
    I = 1.2
    V = 3.0
    m = 2.0
    b = 0.9
    s = lambda u: 4 * u
    t = sp.Symbol('t')
    T = 2.0
    dt = 0.2
    N = int(round(T / dt))
    time_points = np.linspace(0, T, N + 1)

    # Linear damping
    q = 2
    u_exact = I + V * t + q * t**2
    u_e = sp.lambdify(t, u_exact, modules='numpy')
    F = sp.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'linear'), modules='numpy')
    u, t_ = function(I, V, m, b, s, F, time_points, 'linear')
    assert abs(u_e(t_) - u).max() == pytest.approx(0.0, abs=1e-13)

    # Quadratic damping (not supported by the linear-only wrapper)
    if function is _solver_linear_damping_wrapper:
        return

    u_exact = I + V * t
    u_e = sp.lambdify(t, u_exact, modules='numpy')
    F = sp.lambdify(t, lhs_eq(t, m, b, s, u_exact, 'quadratic'),
                    modules='numpy')
    u, t_ = function(I, V, m, b, s, F, time_points, 'quadratic')
    assert abs(u_e(t_) - u).max() == pytest.approx(0.0, abs=1e-13)
