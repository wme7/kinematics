    for n in range(1, N):
        if damping == 'linear':
            u[n+1] = (2*m*u[n] + (b*dt/2 - m)*u[n-1] +
                      dt**2*(F[n] - s(u[n])))/(m + b*dt/2)
        elif damping == 'quadratic':
            u[n+1] = (2*m*u[n] - m*u[n-1] +
                      b*u[n]*abs(u[n] - u[n-1]) -
                      dt**2*(s(u[n]) - F[n])) / \
                     (m + b*abs(u[n] - u[n-1]))
    return u, t
