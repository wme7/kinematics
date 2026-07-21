from numpy import *

def frequency_analysis(u, t):
    A = fft.fft(u)
    A = 2*A
    dt = t[1] - t[0]
    N = t.size
    freq = arange(N/2, dtype=float)/N/dt
    A = abs(A[0:freq.size])/N
    tol = 0.05*A.max()
    for i in range(len(A) - 1, 0, -1):
        if A[i] > tol:
            break
    return freq[:i+1], A[:i+1]
