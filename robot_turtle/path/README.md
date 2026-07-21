# Map Generator and Loader

This folder provides functions for generating waypoints in square or circular shape, and loading / plotting waypoints from CSV map files.

## Functions

`square_path_generator` generates a square-shaped path with waypoints at defined intervals. `circle_path_generator` generates a circle-shaped path with waypoints evenly distributed along the circumference.

```python
waypoints = square_path_generator(x=0, y=0, b=20, step=5)
```

Note that `x` and `y` in `square_path_generator` are the initial position, while in `circle_path_generator` they are the center of the circle. Make sure the robot is initialized at the correct starting position.

Use `load_map` to load waypoints from a CSV file. Each file has an `x,y` header and one waypoint per row:

```csv
x,y
50,50
67,49
85,48
```

```python
from path_generator import load_map, plot_path, plot_all_maps

waypoints = load_map("data/path0.csv")
plot_path("data/path0.csv")         # single path
plot_all_maps()                     # overview of all paths in data/
```

## CLI

Plot a single path or the full overview:

```bash
python -m path_generator.loader -m data/path0.csv
python -m path_generator.loader -o paths_overview.png --no-show
```

## Examples

Example paths under `data/` were generated for comparing different controllers.
Load any `path*.csv` with `load_map` and run a tracking mission as needed.

![image](./paths_overview.png)
