import numpy as np
from numpy import sin, pi
from solver import solver

def F(t):
    return A*sin(pi*t)          # sinusoidal forcing

def s(u):
    return k*(0.2*u + 1.5*u**3)  # nonlinear spring

A = 0.25
k = 2
t = np.linspace(0, 100, 10001)
u, t = solver(I=0.1, V=0, m=2, b=0.5, s=s, F=F, t=t,
              damping='quadratic')
