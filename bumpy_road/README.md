# Bumpy road / vehicle damper

This folder simulates a simple **mechanical engineering** problem:

a vehicle (mass–spring–damper) driving at constant speed over a bumpy road. The road height h(x) becomes a vertical forcing of the suspension, and we compute the vertical displacement u(t) of the vehicle. 

The goal is to let you run and explore real scientific Python, even if you are new to programming.

## The physical idea (short)

1. A road profile gives height h versus distance x.
2. The vehicle moves at constant speed v, so x = v t.
3. Vertical acceleration of the road contact leads to a force on the
  mass–spring–damper model
   
   m u'' + b u' + k u = F(t).
   
4. We solve this ODE in time and look at how “bumpy” the ride feels
  (for example via the size of u).

You do **not** need to derive everything on day one. First learn to **run** the codes, then open the files and connect symbols to the model.

## Data files (CSV)

Road profiles are stored as **CSV** (comma-separated values), easy to open in Excel or a text editor.


| File             | Meaning                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| `draw_bumpy.csv` | Short sample: columns `x,h` (one road segment for sketches / inspection) |
| `bumpy.csv`      | Generated file: columns `x,h0,h1,...` (several road realizations)        |


`bumpy.csv` is created by a script below; it is not committed to git
(it can be large).

## Setup with `uv`

1. Install [uv](https://docs.astral.sh/uv/) if needed.
2. Open a terminal and go to the **project root** (folder with
  `pyproject.toml`):
3. Enter this folder:
  ```bash
   cd bumpy_road
  ```

All commands below assume you are inside `bumpy_road/` and use:

```bash
uv run python <script>.py
```

---



## Suggested first run (students)



### Step 1 — Look at a small road sample

```bash
uv run python -c "import numpy as np; d=np.loadtxt('draw_bumpy.csv', delimiter=',', skiprows=1); print(d.shape); print(d[:3])"
```

You should see many rows with two columns: distance `x` [m] and height
`h` [m].

### Step 2 — Generate full road profiles

```bash
uv run python generate_road_profiles.py
```

This writes `bumpy.csv` (several bumpy roads along a long distance).

### Step 3 — Plot the roads (optional)

```bash
uv run python plot_roads.py
```

A figure window opens; close it to return to the terminal. A file
`road_profiles.png` is also saved.

### Step 4 — Simulate the vehicle

```bash
uv run python bumpy.py
```

Useful options:

```bash
uv run python bumpy.py --help
uv run python bumpy.py --v 8 --b 100
uv run python bumpy.py --roadfile bumpy.csv
```

The script prints RMS displacement values and writes `bumpy.res`
(results for later plotting).

### Step 5 — Explore results (optional)

After a successful `bumpy.py` run:

```bash
uv run python explore.py
```

(You may pass a start time, e.g. `uv run python explore.py 180`.)

### Step 6 — Watch an animation (optional)

A Matplotlib remake of the old PySketcher movie (historical file:
`bumpy_road_fig.py`, do not run that one):

```bash
uv run python bumpy_road_anim.py
```

This writes `bumpy_road.gif` and `bumpy_road.mp4` in the current folder.
Useful options:

```bash
uv run python bumpy_road_anim.py --help
uv run python bumpy_road_anim.py --frames 60 --fps 10
uv run python bumpy_road_anim.py --roadfile draw_bumpy.csv
uv run python bumpy_road_anim.py --roadfile bumpy.csv --profile 0
uv run python bumpy_road_anim.py --mp4 ''          # GIF only
uv run python bumpy_road_anim.py --show            # also open a window
```

By default the animation uses a built-in sine-shaped road. With
`--roadfile` it loads a CSV (`x,h` or `x,h0,h1,...`) and interpolates
height and curvature for the ODE and the drawing.

---



## Main source files


| File                        | Role                                         |
| --------------------------- | -------------------------------------------- |
| `solver.py`                 | Time integrator for m u'' + f(u') + s(u) = F |
| `generate_road_profiles.py` | Build synthetic bumpy roads → `bumpy.csv`    |
| `bumpy.py`                  | Load road CSV, build force, solve for u(t)   |
| `plot_roads.py`             | Plot height profiles from `bumpy.csv`        |
| `explore.py`                | Plot results stored in `bumpy.res`           |
| `symbolic.py`               | SymPy checks for the vibration ODE           |
| `session.py`                | Short interactive-style solver demos         |
| `timings.py`                | Longer run / performance check               |
| `bumpy_road_anim.py`        | Matplotlib GIF/MP4 animation of the vehicle  |
| `bumpy_road_fig.py`         | Historical PySketcher script (not for 3.14)  |
| `tests/test_bumpy.py`       | Automated tests for acceleration / solver    |
| `draw_bumpy.csv`            | Small `x,h` sample for inspection            |


Cython extras (`setup.py`, `make_cython.sh`) are optional and not
required for the first run.

## Clean generated files

```bash
./clean.sh
```

removes local outputs such as `bumpy.csv`, `bumpy.res`, and plots.

## After this folder

If you are still learning Python basics, go back to
`[../python_intro/](../python_intro/)`.  
For sparse matrices / finite differences, see
`[../scipy_intro/](../scipy_intro/)`.