import numpy as np

def solver(I, V, m, b, s, F, t, damping='linear'):
    """Solve m*u'' + f(u') + s(u) = F on the mesh t."""
    N = t.size - 1
    dt = t[1] - t[0]
    u = np.zeros(N+1)
    if callable(F):
        F = F(t)
    else:
        F = np.asarray(F)

    u[0] = I
    if damping == 'linear':
        u[1] = u[0] + dt*V + \
               dt**2/(2*m)*(-b*V - s(u[0]) + F[0])
    elif damping == 'quadratic':
        u[1] = u[0] + dt*V + \
               dt**2/(2*m)*(-b*V*abs(V) - s(u[0]) + F[0])
