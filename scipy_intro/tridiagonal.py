"""Learning goals:
- Build a tridiagonal sparse matrix with scipy.sparse.diags_array
- Solve Ax = b with sparse and dense linear algebra
- Compare sparse @ / spsolve with NumPy dense solve
"""

import numpy as np
from scipy.sparse import diags_array
from scipy.sparse.linalg import spsolve

N = 6
# Off-diagonals have length N-1 (no padding, unlike the old spdiags API)
lower = np.linspace(-1, -(N - 1), N - 1)
main = -2 * np.ones(N)
upper = np.linspace(2, N, N - 1)
A = diags_array([lower, main, upper], offsets=[-1, 0, 1], format='csc')
A_d = A.toarray()  # make corresponding dense matrix
print(A_d)

# Solve linear system
x = np.linspace(-1, 1, N)  # choose solution
b = A @ x                  # sparse matrix-vector product
x = spsolve(A, b)
print(x)

# Compare with dense matrix computations
b = A_d @ x  # standard matrix-vector product
x = np.linalg.solve(A_d, b)
print(x)
