"""Load robot waypoint maps from CSV and plot them with matplotlib."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_map(filename: str | Path) -> list[tuple[int, int]]:
    """Load waypoints from a CSV file with ``x,y`` columns.

    Parameters
    ----------
    filename:
        Path to a CSV map file (header ``x,y``, one waypoint per row).

    Returns
    -------
    list[tuple[int, int]]
        Sequence of ``(x, y)`` waypoint coordinates.
    """
    data = np.loadtxt(filename, delimiter=",", skiprows=1, dtype=int)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return [(int(x), int(y)) for x, y in data]


def plot_path(
    filename: str | Path,
    *,
    ax: plt.Axes | None = None,
    show: bool = True,
    invert_y: bool = True,
) -> plt.Axes:
    """Plot a waypoint path from a CSV map file.

    Parameters
    ----------
    filename:
        Path to a CSV map file.
    ax:
        Optional matplotlib axes. If omitted, a new figure is created.
    show:
        If True, call ``plt.show()`` when creating a new figure.
    invert_y:
        If True, invert the y-axis (image / screen coordinates).

    Returns
    -------
    matplotlib.axes.Axes
        The axes used for drawing.
    """
    waypoints = load_map(filename)
    xs = [p[0] for p in waypoints]
    ys = [p[1] for p in waypoints]

    own_figure = ax is None
    if own_figure:
        _, ax = plt.subplots(figsize=(6, 6))

    ax.plot(xs, ys, color="gray", linewidth=1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(Path(filename).name)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.6)
    if invert_y:
        ax.invert_yaxis()

    if own_figure and show:
        plt.tight_layout()
        plt.show()

    return ax


def plot_all_maps(
    data_dir: str | Path | None = None,
    *,
    save_path: str | Path | None = None,
    show: bool = True,
) -> plt.Figure:
    """Plot every CSV map in ``data_dir`` as a grid of subplots.

    Parameters
    ----------
    data_dir:
        Directory containing ``path*.csv`` files. Defaults to the package
        ``data/`` folder next to this module.
    save_path:
        Optional path to save the figure (e.g. ``maps.png``).
    show:
        If True, display the figure with ``plt.show()``.

    Returns
    -------
    matplotlib.figure.Figure
        The overview figure.
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent / "data"
    else:
        data_dir = Path(data_dir)

    path_files = sorted(
        data_dir.glob("path*.csv"),
        key=lambda p: int(p.stem.removeprefix("path")),
    )
    if not path_files:
        raise FileNotFoundError(f"No path*.csv files found in {data_dir}")

    n = len(path_files)
    ncols = 4
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3 * nrows), squeeze=False)

    for i, path_file in enumerate(path_files):
        row, col = divmod(i, ncols)
        plot_path(path_file, ax=axes[row, col], show=False)

    for j in range(n, nrows * ncols):
        row, col = divmod(j, ncols)
        axes[row, col].axis("off")

    fig.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    return fig


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot robot waypoint maps from CSV")
    parser.add_argument(
        "-m",
        "--map",
        type=str,
        default=None,
        help="path to a single map CSV (default: plot all maps in data/)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="optional path to save the figure",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="save/plot without opening an interactive window",
    )
    args = parser.parse_args()

    if args.map is not None:
        plot_path(args.map, show=not args.no_show)
        if args.output is not None:
            plt.gcf().savefig(args.output, dpi=150, bbox_inches="tight")
    else:
        plot_all_maps(save_path=args.output, show=not args.no_show)
