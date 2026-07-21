## Why this page exists

The demos make a two-wheeled robot drive around a plane. Under the hood, that motion comes from a small set of equations: how wheel speeds turn into body motion, how body motion turns back into wheel speeds, and how pose updates each time step.

You do not need to memorize every formula. Use this page as a map while you read [`robot/robot.py`](robot/robot.py).

## The differential-drive idea

A differential-drive robot has two wheels that can spin at different speeds. Drive both at the same speed and the robot goes straight. Spin them differently and it turns.

We usually describe the robot’s motion with two body speeds:

- linear velocity $v$ — how fast it moves forward
- angular velocity $\omega$ — how fast it turns (yaw rate)

Those two numbers are linked to the left and right wheel speeds through the wheel radius $r$ and the half-track width $b$ (half the distance between the wheels). In this codebase, `self.b` is that half-track width.

## Forward kinematics

**Forward kinematics** answers: given the wheel speeds, what are $v$ and $\omega$?

$$
v = \frac{r}{2}\,(v_{\mathrm{left}} + v_{\mathrm{right}}),
\qquad
\omega = \frac{r}{2b}\,(v_{\mathrm{left}} - v_{\mathrm{right}})
$$

In matrix form:

$$
\begin{bmatrix}
v \\
\omega
\end{bmatrix}
=
r
\begin{bmatrix}
\frac{1}{2} & \frac{1}{2} \\
\frac{1}{2b} & -\frac{1}{2b}
\end{bmatrix}
\begin{bmatrix}
v_{\mathrm{left}} \\
v_{\mathrm{right}}
\end{bmatrix}
$$

In code (`_forward`), the body velocity is stored as a 3-vector ($v,\,0,\,\omega$), so the middle row is zeros:

```python
def _forward(self):
    mat = np.array([
        [self.wheel_radius / 2, self.wheel_radius / 2],
        [0, 0],
        [self.wheel_radius / (self.b * 2), -self.wheel_radius / (self.b * 2)]
    ])
    self.v = mat @ self.wheel_speeds
```

Average the wheels for forward speed; use their difference for turning.

## Inverse kinematics

**Inverse kinematics** is the other direction: given desired $v$ and $\omega$, what wheel speeds do we need?

With half-track \(b\):

$$
v_{\mathrm{left}} = \frac{1}{r}\,(v + b\,\omega),
\qquad
v_{\mathrm{right}} = \frac{1}{r}\,(v - b\,\omega)
$$

In matrix form (matching the 3-component body velocity used in code):

$$
\begin{bmatrix}
v_{\mathrm{left}} \\
v_{\mathrm{right}}
\end{bmatrix}
=
\frac{1}{r}
\begin{bmatrix}
1 & 0 & b \\
1 & 0 & -b
\end{bmatrix}
\begin{bmatrix}
v \\
0 \\
\omega
\end{bmatrix}
$$

```python
def _inverse(self):
    mat = np.array([
        [1 / self.wheel_radius, 0, self.b / self.wheel_radius],
        [1 / self.wheel_radius, 0, -self.b / self.wheel_radius]
    ])
    self.wheel_speeds = mat @ self.v
```

Controllers typically output $(v, \omega)$; inverse kinematics turns that command into left and right wheel speeds.

## Updating the pose

The robot’s pose is $\mathbf{p} = (x,\,y,\,\theta)^\top$: position in the plane and heading angle $\theta$.

Each simulation step integrates the body velocities over a small time `dt`. Screen coordinates grow rightward in $x$ and **downward** in $y$ (same as most 2D graphics), which is why the update uses $\sin(\theta + \pi/2)$ and $\cos(\theta + \pi/2)$:

```python
def update(self, dt=0.5):
    self._forward()

    mat = dt * np.array([
        [np.sin(self.p[2] + np.pi / 2), 0],
        [np.cos(self.p[2] + np.pi / 2), 0],
        [0, 1]
    ])
    self.p += mat @ self.v[[0, 2], :]
    self._inverse()
```

In words: move a little along the current heading, and rotate a little by $\omega\,\mathrm{d}t$. In matrix form:

$$
\begin{bmatrix}
x \\
y \\
\theta
\end{bmatrix}
= \begin{bmatrix}
x \\
y \\
\theta
\end{bmatrix} + \begin{bmatrix}
\sin(\theta + \pi/2) & 0 \\
\cos(\theta + \pi/2) & 0 \\
0 & 1
\end{bmatrix} \begin{bmatrix}
v \\
\omega
\end{bmatrix} \mathrm{d}t
$$
## Drawing the robot

For visualization, the robot is a small polygon in its body frame (`framework`). Each frame, that outline is rotated by $\theta$ and translated to $(x, y)$:

```python
def _update_polygon(self):
    mat = np.array([
        [ np.cos(self.p[2]), np.sin(self.p[2]), self.p[0]],
        [-np.sin(self.p[2]), np.cos(self.p[2]), self.p[1]],
        [0, 0, 1]
    ])
    self.polygon = (self.framework @ mat.T).astype(int)
```

That is pure geometry for drawing — it does not change the kinematics.

## Where to look next

- Controllers choose $(v, \omega)$: see the README section on PID and MPC, and [`robot/control.py`](robot/control.py).
- The full simulation loop is sketched in the main [README](README.md).

# References

https://medium.com/@koko0915/differential-wheeled-robot-with-python-simulation-80297d60786d
