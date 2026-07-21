"""Learning goals:
- Approximate u''(x) with the central finite-difference stencil
- Build that scheme as a scipy.sparse.linalg.LinearOperator (matvec only)
- Check the operator on a known function against the exact second derivative
"""

import numpy as np
from scipy.sparse.linalg import LinearOperator


def central_second_derivative(n, h):
    """Return a LinearOperator for the 1D central second-difference.

    u holds values at n *interior* grid points. Homogeneous Dirichlet
    values u=0 are assumed just outside both ends, so

        (D2 u)_i = (u_{i-1} - 2 u_i + u_{i+1}) / h^2

    with u_{-1} = u_{n} = 0. This is the classic tridiagonal FD matrix,
    applied without storing the matrix explicitly.
    """

    def matvec(u):
        u = np.asarray(u, dtype=float).ravel()
        y = np.empty(n, dtype=float)
        y[0] = (-2.0 * u[0] + u[1]) / h**2
        y[1:-1] = (u[:-2] - 2.0 * u[1:-1] + u[2:]) / h**2
        y[-1] = (u[-2] - 2.0 * u[-1]) / h**2
        return y

    return LinearOperator(shape=(n, n), matvec=matvec, dtype=float)


def main():
    # Interior grid on (0, 1) with spacing h and u(0) = u(1) = 0
    n = 20
    h = 1.0 / (n + 1)
    x = np.arange(1, n + 1) * h

    D2 = central_second_derivative(n, h)

    # Test function with known second derivative: u = sin(pi x)
    u = np.sin(np.pi * x)
    u_xx_exact = -(np.pi**2) * np.sin(np.pi * x)
    u_xx_fd = D2 @ u  # LinearOperator supports matvec via @

    err = np.max(np.abs(u_xx_fd - u_xx_exact))
    print(f'n = {n}, h = {h:.4f}')
    print(f'max |D2 u - u_xx| = {err:.6e}')
    print('tip: refine the grid (larger n) and watch the error drop ~ O(h^2)')


if __name__ == '__main__':
    main()
