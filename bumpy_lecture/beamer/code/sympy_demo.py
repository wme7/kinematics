import sympy as sp

t, m, b, k = sp.symbols('t m b k', real=True, positive=True)
u = sp.Function('u')

ode = m*sp.diff(u(t), t, 2) + b*sp.diff(u(t), t) + k*u(t)
print(ode)

# Manufactured forcing for a chosen exact solution
I, V, q = 1.2, 3.0, 2.0
u_exact = I + V*t + q*t**2
F = sp.lambdify(t, ode.subs(u(t), u_exact).doit(), 'numpy')
