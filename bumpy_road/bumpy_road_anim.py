"""Learning goals:
- Visualize a mass–spring–damper vehicle on a bumpy road
- Drive Matplotlib artists with matplotlib.animation.FuncAnimation
- Export the animation as GIF (Pillow) and MP4 (imageio-ffmpeg)
- Optionally load a measured/generated road profile from CSV

This is a modern alternative to the historical pysketcher script
bumpy_road_fig.py (kept for reference only).
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch

from solver import solver

# Default drawing size (analytic road); CSV profiles may auto-scale R
R_DEFAULT = 0.50
H = 2.0
VIEW_LEFT_R = 5.0
VIEW_RIGHT_R = 15.0


def configure_matplotlib_fonts():
    """Use LaTeX fonts when a latex binary is available; else MathText."""
    if shutil.which('latex'):
        plt.rcParams.update({
            'text.usetex': True,
            'font.family': 'serif',
            'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
            'axes.labelsize': 16,
            'axes.titlesize': 16,
            'legend.fontsize': 16,
        })
        return True
    # Fallback: Matplotlib's built-in math rendering (no system LaTeX)
    plt.rcParams.update({
        'text.usetex': False,
        'mathtext.fontset': 'cm',
        'font.family': 'serif',
    })
    return False


def analytic_road():
    """Smooth sinusoidal road: h(x), h''(x), and an x-span for the trip."""
    Amplitude = 0.1
    Frequency = np.pi / 2
    def h(x):
        return Amplitude * np.sin(Frequency * x)

    def hxx(x):
        return -Amplitude * (Frequency**2) * np.sin(Frequency * x)

    return h, hxx, 0.0, 40.0


def load_road_csv(path, profile=0):
    """Load road CSV with columns x,h or x,h0,h1,...

    Returns h(x), h''(x) callables and the x-interval covered by the file.
    """
    path = Path(path)
    data = np.loadtxt(path, delimiter=',', skiprows=1)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(f'{path} must have columns x,h... ; got shape {data.shape}')

    x = np.asarray(data[:, 0], dtype=float)
    col = 1 + profile
    if col >= data.shape[1]:
        raise ValueError(
            f'profile={profile} needs column {col}, but file has '
            f'only {data.shape[1]} columns')
    h_tab = np.asarray(data[:, col], dtype=float)

    # Sort and drop duplicate x (interp requires increasing x)
    order = np.argsort(x)
    x, h_tab = x[order], h_tab[order]
    uniq = np.concatenate([[True], np.diff(x) > 0])
    x, h_tab = x[uniq], h_tab[uniq]

    # Numerical second derivative on the table (same idea as bumpy.py)
    dh = np.gradient(h_tab, x)
    d2h = np.gradient(dh, x)

    def h(xq):
        return np.interp(xq, x, h_tab)

    def hxx(xq):
        return np.interp(xq, x, d2h)

    return h, hxx, float(x[0]), float(x[-1])


def zigzag_spring(x0, y0, x1, y1, n_windings=6, width=0.6):
    """Return (xs, ys) for a simple zigzag spring from (x0,y0) to (x1,y1)."""
    n = 2 * n_windings + 2
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    dx, dy = x1 - x0, y1 - y0
    length = np.hypot(dx, dy) + 1e-12
    px, py = -dy / length, dx / length
    amp = np.zeros(n)
    amp[1:-1] = width * (1 - 2 * (np.arange(1, n - 1) % 2))
    return xs + amp * px, ys + amp * py


def choose_wheel_radius(x_min, x_max, h_fun, R=None):
    """Pick a wheel radius that fits the road scale (CSV bumps are often small)."""
    if R is not None:
        return R
    xs = np.linspace(x_min, x_max, 400)
    hs = h_fun(xs)
    span = max(x_max - x_min, 1e-6)
    bump = max(np.ptp(hs), 1e-6)
    # Visible wheel: a few bump heights, but not huge vs the road length
    return float(np.clip(max(3.0 * bump, 0.02 * span), 0.05, 0.15 * span))


def simulate(h, hxx, x_min, x_max, v=2.0, m=2.0, b=0.2, k=1.5, n=400):
    """Solve vertical vibration while the vehicle moves at speed v on h(x)."""
    # Stay slightly inside the tabulated interval for safe interpolation
    margin = 0.01 * (x_max - x_min)
    x0, x1 = x_min + margin, x_max - margin
    T = (x1 - x0) / v
    t = np.linspace(0.0, T, n + 1)
    x = x0 + v * t
    s = lambda u: k * u
    # Correct kinematic excitation: a = h''(x) * v^2
    F = -m * hxx(x) * v**2
    u, t = solver(I=0, V=0, m=m, b=b, s=s, F=F, t=t, damping='linear')
    return t, u, x0


def build_animation(t, u, v, x0, h, m, b, k, R, n_frames=120, fps=15):
    """Create a FuncAnimation of the vehicle on the road."""
    u_amp = max((u.max() - u.min()) / 2, 1e-6)
    # Scale suspension motion to a fraction of the wheel size for visibility
    u_scaled = (0.6 * R) * u / u_amp

    idx = np.linspace(0, len(t) - 1, n_frames, dtype=int)
    t_f = t[idx]
    u_f = u_scaled[idx]
    x_f = x0 + v * t_f
    y_f = h(x_f)

    ds = np.hypot(np.diff(x_f, prepend=x_f[0]), np.diff(y_f, prepend=y_f[0]))
    arc = np.cumsum(ds)

    view_left = VIEW_LEFT_R * R
    view_right = VIEW_RIGHT_R * R
    trace_y0 = y_f.mean() + 8 * R

    fig, ax = plt.subplots(figsize=(9.6, 4.8))  # 960x480 px at dpi=100
    ax.set_aspect('equal')
    ax.set_xlabel(r'$x$ [m]')
    ax.set_ylabel(r'$y$ [m]')
    ax.set_title(rf'$m={m:g}$, $b={b:g}$, $k={k:g}$, $v={v:g}$ [m/s]')

    x_road = np.linspace(x_f[0] - view_left, x_f[-1] + view_right, 800)
    road_y = h(x_road)
    road_line, = ax.plot(x_road, road_y, 'g-', lw=2, label='road')

    spring_rest = 3 * R
    mass_height = 1.5 * R
    u_vis_max = float(np.max(u_f))
    # Tallest point of the drawn vehicle (road → wheel → spring → mass)
    vehicle_top = (
        float(np.max(road_y))
        + 2 * R
        + spring_rest
        + u_vis_max
        + mass_height
    )
    # Keep the blue u(t) trace in view as well
    y_min = float(np.min(road_y)) - 1.0
    y_max = max(vehicle_top, float(np.max(trace_y0 + u_f))) + 0.5 * R
    ax.set_ylim(y_min, y_max)

    # ODE in a box at the centre of the axes (axes fraction coords)
    ax.text(
        0.6, 0.5,
        r'$m\,\ddot{u} + b\,\dot{u} + k\,u = F(t)$',
        transform=ax.transAxes,
        ha='center', va='center',
        fontsize=14,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='0.3', alpha=0.9),
        zorder=10,
    )

    trace_line, = ax.plot([], [], 'b-', lw=1, alpha=0.7, label=r'$u(t)$ (scaled)')

    wheel = Circle((0, 0), R, facecolor='tomato', edgecolor='black',
                   lw=1.5, zorder=3)
    spoke1, = ax.plot([], [], 'k-', lw=1.5, zorder=4)
    spoke2, = ax.plot([], [], 'k-', lw=1.5, zorder=4)
    spring_line, = ax.plot([], [], 'k-', lw=1.5, zorder=2)
    mass = FancyBboxPatch(
        (0, 0), 3 * R, mass_height,
        boxstyle='round,pad=0.02,rounding_size=0.15',
        facecolor='0.15', edgecolor='black', lw=1.2, zorder=3,
    )
    ax.add_patch(wheel)
    ax.add_patch(mass)
    ax.legend(loc='upper right')

    def update(frame):
        x = x_f[frame]
        y = y_f[frame]
        u_vis = u_f[frame]
        angle = -arc[frame] / R

        cx, cy = x, y + R
        wheel.center = (cx, cy)

        c, s_ = np.cos(angle), np.sin(angle)
        spoke1.set_data([cx - R * s_, cx + R * s_],
                        [cy - R * c, cy + R * c])
        spoke2.set_data([cx - R * c, cx + R * c],
                        [cy + R * s_, cy - R * s_])

        spring_len = spring_rest + u_vis
        y_spring_top = cy + R + spring_len
        xs, ys = zigzag_spring(cx, cy + R, cx, y_spring_top,
                               n_windings=6, width=0.55 * R)
        spring_line.set_data(xs, ys)

        mass.set_x(cx - 1.5 * R)
        mass.set_y(y_spring_top)

        trace_line.set_data(x_f[:frame + 1], trace_y0 + u_f[:frame + 1])

        ax.set_xlim(x - view_left, x + view_right)
        return wheel, spoke1, spoke2, spring_line, mass, trace_line, road_line

    anim = FuncAnimation(
        fig, update, frames=n_frames, interval=1000 / fps, blit=False,
    )
    return fig, anim, fps, n_frames


def save_gif(anim, path: Path, fps: int):
    path = Path(path)
    print(f'Writing {path} ...')
    anim.save(path, writer=PillowWriter(fps=fps))
    print(f'Saved GIF: {path.resolve()}')


def save_mp4(fig, anim, path: Path, fps: int, n_frames: int):
    """Save MP4 via imageio-ffmpeg (bundled ffmpeg; no system install needed)."""
    import imageio.v2 as imageio

    path = Path(path)
    print(f'Writing {path} ...')
    with imageio.get_writer(path, fps=fps, codec='libx264', quality=8) as writer:
        for i in range(n_frames):
            anim._func(i)
            fig.canvas.draw()
            buf = np.asarray(fig.canvas.buffer_rgba())
            writer.append_data(buf[:, :, :3])
    print(f'Saved MP4: {path.resolve()}')


def main():
    parser = argparse.ArgumentParser(
        description='Matplotlib animation of vehicle on a bumpy road')
    parser.add_argument(
        '--roadfile', type=str, default='',
        help='CSV road profile (x,h or x,h0,h1,...). '
             'Default: built-in sine road')
    parser.add_argument(
        '--profile', type=int, default=0,
        help='which height column to use: 0->h/h0, 1->h1, ...')
    parser.add_argument('--gif', type=str, default='bumpy_road.gif',
                        help='output GIF filename (empty string to skip)')
    parser.add_argument('--mp4', type=str, default='bumpy_road.mp4',
                        help='output MP4 filename (empty string to skip)')
    parser.add_argument('--frames', type=int, default=100,
                        help='number of animation frames')
    parser.add_argument('--fps', type=int, default=12, help='frames per second')
    parser.add_argument('--v', type=float, default=2.0, help='vehicle speed')
    parser.add_argument('--R', type=float, default=None,
                        help='wheel radius [m] (auto for CSV if omitted)')
    parser.add_argument('--show', action='store_true',
                        help='show interactive window after saving')
    args = parser.parse_args()

    using_latex = configure_matplotlib_fonts()
    if using_latex:
        print('Matplotlib text: LaTeX (usetex)')
    else:
        print('Matplotlib text: MathText fallback (latex not found)')

    m, b, k = 2.0, 0.2, 1.5
    if args.roadfile:
        h, hxx, x_min, x_max = load_road_csv(args.roadfile, profile=args.profile)
        print(f'Road from {args.roadfile} (profile {args.profile}): '
              f'x in [{x_min:.3g}, {x_max:.3g}]')
        R = choose_wheel_radius(x_min, x_max, h, R=args.R)
    else:
        h, hxx, x_min, x_max = analytic_road()
        R = args.R if args.R is not None else R_DEFAULT

    t, u, x0 = simulate(h, hxx, x_min, x_max, v=args.v, m=m, b=b, k=k, n=500)
    fig, anim, fps, n_frames = build_animation(
        t, u, args.v, x0, h, m, b, k, R,
        n_frames=args.frames, fps=args.fps,
    )

    anim._func(0)
    fig.canvas.draw()

    if args.gif:
        save_gif(anim, Path(args.gif), fps)

    if args.mp4:
        try:
            save_mp4(fig, anim, Path(args.mp4), fps, n_frames)
        except Exception as exc:
            print(f'Could not write MP4 ({exc}). GIF may still be available.')

    if args.show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == '__main__':
    main()
