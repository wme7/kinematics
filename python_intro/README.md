# Python intro (self-study)

Short scripts that introduce Python for scientific computing, using the
simple kinematics formula

\[
s(t) = v_0 t + \tfrac{1}{2} a t^2
\]

Work through the files **in order**. Each file starts with a short
*Learning goals* docstring — read that first, then run the script.

## Before you start

You need [uv](https://docs.astral.sh/uv/) installed (it installs Python
and packages for you).

1. Open a terminal.
2. Go to the **project root** (the folder that contains `pyproject.toml`):

   ```bash
   cd /path/to/kinematics
   ```

3. Install dependencies once:

   ```bash
   uv sync
   ```

4. Enter the tutorial folder:

   ```bash
   cd python_intro
   ```

From here on, run scripts with:

```bash
uv run python <script>.py
```

Example:

```bash
uv run python distance.py
```

You do **not** need to activate a virtual environment by hand: `uv run`
uses the project environment created by `uv sync`.

### Plot windows

Scripts `plot1.py` … `plot3_vec.py` open a figure window. Close the window
to return to the terminal. Generated files such as `myplot.png` and
`table*.dat` are ignored by git (they are local outputs).

---

## Suggested sequence

| Step | File | What you learn |
|------|------|----------------|
| 1 | `distance.py` | Expressions, variables, printing numbers |
| 2 | `list.py` | Lists and `for` over elements |
| 3 | `while_demo.py` | Compact `while` loop |
| 4 | `while.py` | Same idea; notice floating-point drift when adding `dt` |
| 5 | `while_list.py` | Collect results with `append`, print a table |
| 6 | `for_list.py` | `for` + `range` when the number of steps is known; `zip` |
| 7 | `for_array.py` | NumPy arrays and a vectorized formula |
| 8 | `for_file_read_input.py` | Read parameters from YAML; write results to a file |
| 9 | `plot1.py` | First Matplotlib plot; axis labels with units |
| 10 | `plot2.py` | Two curves, styles, and a legend |
| 11 | `plot3.py` | Piecewise function with an explicit Python loop |
| 12 | `plot3_vec.py` | **Same physics**, no Python loop (`np.where`) |

Compare steps 11 and 12 carefully: the math is identical; only the way
you evaluate it over many time samples changes.

### Input file for step 8

`for_file_read_input.py` reads `input.yaml`:

```yaml
v0: 2.0
a: 0.2
dt: 0.1
interval: [0, 2]
```

Edit those values, run the script again, and check `table1.dat` /
`table2.dat`.

---

## File reference

| File | Role |
|------|------|
| `distance.py` | Compute and print one `s` value |
| `list.py` | Iterate a small list |
| `while_demo.py` / `while.py` | Time-stepping with `while` |
| `while_list.py` | Build `t_values` / `s_values` lists |
| `for_list.py` | Same table with `for` and `zip` |
| `for_array.py` | Same idea with NumPy |
| `input.yaml` | Parameters for the I/O example |
| `for_file_read_input.py` | YAML in → table files out |
| `plot1.py` | Single curve `s(t)` |
| `plot2.py` | Compare two accelerations |
| `plot3.py` | Piecewise `s(t)` via a Python loop |
| `plot3_vec.py` | Piecewise `s(t)` vectorized |

---

## After this folder

When you are comfortable with the sequence above, try:

- [`../scipy_intro/`](../scipy_intro/) — sparse matrices and finite-difference `LinearOperator`
- [`../bumpy_road/`](../bumpy_road/) — bumpy-road / damper simulation (more advanced)

See [`../scipy_intro/README.md`](../scipy_intro/README.md) for the SciPy sequence.

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `uv: command not found` | Install uv: https://docs.astral.sh/uv/getting-started/installation/ |
| `ModuleNotFoundError` | Run `uv sync` from the project root, then use `uv run python …` |
| Wrong folder | Scripts that read `input.yaml` must be run from `python_intro/` |
| Plot does not appear | Normal in some remote/SSH setups; the script still saves `myplot.png` |
| Want to change Python version | The project pins Python in `.python-version`; `uv sync` respects it |
