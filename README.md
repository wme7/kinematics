# Kinematics

Modern Python rewrites of classic **kinematics and dynamics** teaching demos for mechanical engineering students.

The idea is simple: run a short simulation, watch the motion, then open the code and connect what you see to the equations you already know from class. You do **not** need to be a programmer first — start by running, then dig deeper.

## Two examples to get curious

### Vehicle on a bumpy road

A mass–spring–damper rides over a wavy road profile. The road height becomes a time-varying force, and the vertical motion \(u(t)\) follows

$$
m\,\ddot{u} + b\,\dot{u} + k\,u = F(t).
$$

![Vehicle damper on a bumpy road](./bumpy_road/bumpy_road.gif)

Explore the full folder: **[bumpy_road/](bumpy_road/)** · guide: **[bumpy_road/README.md](bumpy_road/README.md)**

### Differential-drive robot path tracking

A two-wheeled robot follows a planned path in the plane. Controllers (PID, and optionally MPC) choose forward speed \(v\) and yaw rate \(\omega\) from the pose \((x, y, \theta)\).

![Robot path tracking](./robot_turtle/path6.gif)

Explore the full folder: **[robot_turtle/](robot_turtle/)** · guide: **[robot_turtle/README.md](robot_turtle/README.md)**

## Folders

| Folder | Contents |
|--------|----------|
| [`python_intro/`](python_intro/) | Beginner Python self-study (start here if you are new to coding) |
| [`scipy_intro/`](scipy_intro/) | SciPy sparse matrices and `LinearOperator` finite-difference example |
| [`bumpy_road/`](bumpy_road/) | Bumpy-road / vehicle damper simulation (ODE + animation) |
| [`robot_turtle/`](robot_turtle/) | Differential-drive robot, path tracking, PID / MPC demos |

## Quick start (students)

Install [uv](https://docs.astral.sh/uv/), then from this directory:

```bash
uv sync
```

**If you are new to Python**, begin with the intro scripts:

```bash
cd python_intro
uv run python distance.py
```

**Try a kinematics demo next:**

```bash
# vehicle on a bumpy road — solve, then animate (writes bumpy_road.gif)
cd bumpy_road
uv run python bumpy.py
uv run python bumpy_road_anim.py

# path-tracking robot (from repo root after uv sync)
cd ../robot_turtle
uv run python robot_interactive.py -t square
uv run python robot_path.py -p path/data/path6.csv --gif path6.gif
```

- Beginner Python: **[python_intro/README.md](python_intro/README.md)**
- SciPy FD / sparse: **[scipy_intro/README.md](scipy_intro/README.md)**
- Vehicle on bumpy road: **[bumpy_road/README.md](bumpy_road/README.md)**
- Mobile robot path tracking: **[robot_turtle/README.md](robot_turtle/README.md)**
