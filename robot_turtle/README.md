# Robot turtle — differential-drive path tracking

This folder simulates a simple **two-wheeled (differential-drive) mobile robot** that follows a sequence of waypoints on a flat plane.

The goal is to connect kinematics and basic feedback control to a short Python animation: you see the robot move, turn, and leave a trail while a controller chooses forward speed and yaw rate.

You do **not** need to derive every equation on day one. First **run** the demos, then open the source files and match symbols to the model.

## The physical idea (short)

1. The robot has pose \(\mathbf{p} = (x, y, \theta)^\top\): position in the plane and heading angle \(\theta\).
2. Commands are a **linear speed** \(v\) (along the robot’s forward axis) and an **angular speed** \(\omega\) (yaw rate).
3. Those body speeds map to **left / right wheel speeds** (and back) through the wheel radius and half-track width \(b\). That is the classic differential-drive kinematics.
4. A **controller** looks at the next waypoint, computes distance and heading error, and outputs \((v, \omega)\).
5. Each time step updates the pose; the window redraws the robot polygon, the planned path, and the trail.

Screen coordinates: \(x\) grows to the right, \(y\) grows **downward** (same convention as most 2D graphics).

## What you will see

| Color / item | Meaning |
| ------------ | ------- |
| Green robot (`robot_interactive.py`) | Single robot under PID control |
| Orange robot (`robot_path.py`) | PID controller |
| Cyan robot (`robot_path.py`) | MPC controller (same path, for comparison) |
| Grey polyline | Waypoints / planned path |
| Colored dotted trail | History of the robot center |

Press **`q`** in the window to quit.

## Setup with `uv`

1. Install [uv](https://docs.astral.sh/uv/) if needed.
2. From the **project root** (folder with `pyproject.toml`), sync dependencies once:

```bash
uv sync
```

3. Enter this folder:

```bash
cd robot_turtle
```

All commands below assume you are inside `robot_turtle/` and use:

```bash
uv run python <script>.py ...
```

## Suggested first runs (students)

### 1 — Follow a square path (PID only)

```bash
uv run python robot_interactive.py -t square
```

A green robot starts at a corner and visits waypoints that form a square.

### 2 — Follow a circle

```bash
uv run python robot_interactive.py -t circle
```

### 3 — Draw your own waypoints with the mouse

```bash
uv run python robot_interactive.py -t cursor
```

- **Left click**: add a waypoint  
- **Right click**: remove the last waypoint  
- The robot tracks the list in order (PID)

Default mode is `cursor` if you omit `-t`.

### 4 — Compare PID and MPC on a stored map

```bash
uv run python robot_path.py -p path/data/path0.csv
```

Two robots start at the same place and chase the **same** CSV waypoints: orange = PID, cyan = MPC. Try other files under `path/data/` (`path1.csv` … `path10.csv`).

To save an animated GIF (Pillow, same idea as `bumpy_road`), pass `--gif`. The run stops automatically when both robots finish the path (or press `q` earlier):

```bash
uv run python robot_path.py -p path/data/path0.csv --gif out.gif
uv run python robot_path.py -p path/data/path0.csv --gif out.gif --fps 24
```

More detail on CSV maps and plotting: **[path/README.md](path/README.md)**.

## Controllers (intuition)

Both controllers output \((v, \omega)\) for the robot model in `robot/robot.py`.

### PID ([`robot/control.py`](robot/control.py))

- **Distance error** → drives linear speed \(v\) (go closer to the target).
- **Heading error** (angle to the target vs current \(\theta\)) → drives \(\omega\) (turn toward the target).
- Gains \(K_p, K_i, K_d\) weight present error, accumulated error, and rate of change of error.

When the robot is close enough to the current waypoint (threshold in pixels), the demo advances to the next one.

### MPC (same file)

- Looks a few steps ahead (prediction **window**).
- Chooses a short sequence of \((v, \omega)\) that reduces predicted distance to the target while penalizing large or rapidly changing inputs.
- Uses a numerical optimizer (`scipy.optimize.minimize`); it is heavier than PID, which is why the dual demo is interesting to watch.

You can change gains / window size in the entry scripts and re-run to see the effect.

## How a simulation step works

```text
waypoints  →  controller (PID or MPC)  →  (v, ω)
                                              ↓
                                    Robot.set_robot_speeds
                                              ↓
                                    Robot.update(dt)   # integrate pose
                                              ↓
                                    Application redraw (pygame)
```

Interactive demo loop: [`robot_interactive.py`](robot_interactive.py) (`tracking`).  
Side-by-side demo: [`robot_path.py`](robot_path.py) (`Pipeline`).

## Folder layout

| Path | Role |
| ---- | ---- |
| [`robot_interactive.py`](robot_interactive.py) | Square / circle / mouse-drawn path with one PID robot |
| [`robot_path.py`](robot_path.py) | Load a CSV map; run PID and MPC together |
| [`robot/robot.py`](robot/robot.py) | Differential-drive kinematics and drawable outline |
| [`robot/control.py`](robot/control.py) | `PID` and `MPC` controllers |
| [`path/`](path/) | Waypoint generators, CSV loader, sample maps |
| [`utils/app.py`](utils/app.py) | pygame window: draw robot, path, trail; handle keys/mouse |
| [`utils/waypoints.py`](utils/waypoints.py) | Mouse add/remove waypoints |
| [`utils/compute.py`](utils/compute.py) | Distance and angle helpers |

## Notes for reading the code

- **State** `Robot.state` returns pose \(\mathbf{p}\) and velocity \(\mathbf{v}\). Pose components are \(x\), \(y\), \(\theta\).
- **`set_robot_speeds(v, w)`** sets body linear/angular speed; **`set_wheel_speeds`** sets left/right wheels. Forward / inverse maps live in `_forward` / `_inverse`.
- Graphics use **RGB** colors and the pygame window in `utils/app.py`. Kinematics stay in NumPy; drawing does not need OpenCV.
- Time step in the demos is often `dt = 0.5` (simulation units per frame), not necessarily seconds of wall-clock time. The display aims for roughly 30 frames per second.

## What to try next

1. Change PID gains in `robot_interactive.py` and watch overshoot or sluggish turning.
2. Build a short path in `cursor` mode, then compare behavior to `square` / `circle`.
3. Run several `path/data/path*.csv` files in `robot_path.py` and note how MPC and PID trails differ on sharp corners.
4. Open `robot/robot.py` and identify where \(v\) and \(\omega\) update \(x\), \(y\), and \(\theta\).
