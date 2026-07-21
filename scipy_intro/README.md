# SciPy intro

Short examples beyond basic Python / NumPy. Do
[`../python_intro/`](../python_intro/) first if you are new to Python.

## Setup

From the project root (folder with `pyproject.toml`):

```bash
uv sync
cd scipy_intro
```

Run a script with:

```bash
uv run python <script>.py
```

## Suggested order

| Step | File | What you learn |
|------|------|----------------|
| 1 | `tridiagonal.py` | Build a tridiagonal sparse matrix with `diags_array`, solve with sparse and dense methods |
| 2 | `finite_difference_operator.py` | Central finite-difference second derivative as a `LinearOperator` (no full matrix stored) |

## File reference

| File | Role |
|------|------|
| `tridiagonal.py` | Explicit sparse matrix `A`, then `A @ x` and `spsolve` |
| `finite_difference_operator.py` | Same FD idea as a matvec-only `LinearOperator`; test on \(u=\sin(\pi x)\) |

## Why `LinearOperator`?

Iterative solvers (and many PDE codes) only need products `A @ v`.
A `LinearOperator` lets you define that product with a function—useful when
assembling or storing the full matrix is expensive.

## Next

Continue with the bumpy-road / vehicle damper codes in [`../bumpy_road/`](../bumpy_road/).
