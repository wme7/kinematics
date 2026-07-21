import os
import argparse
from pathlib import Path

import numpy as np

from typing import Callable

from utils import Application
from robot import Robot, PID, MPC

from path import load_map
from utils import compute_distance


class Pipeline(object):
    def __init__(
        self,
        robot: Robot,
        waypoints: list[tuple[int, int]],
        update_func: Callable[[np.ndarray, tuple[int, int]], tuple[float, float]],
    ) -> None:
        self.robot: Robot = robot
        self.ctrl: Callable = update_func

        self.waypoints: list = waypoints
        self.index: int = 0
        self.history: list = []
        self.error: list = []

        self.times: list = []
        self.current_time: float = 0

    @property
    def finished(self) -> bool:
        return self.index >= len(self.waypoints)

    def update(self, dt: float, threshold: int = 30) -> None:
        if self.index < len(self.waypoints):
            p, _ = self.robot.state
            self.history.append((int(p[0, 0]), int(p[1, 0])))

            target = self.waypoints[self.index]
            v, w = self.ctrl(p, target)
            d: float = compute_distance(tuple(p[:2].flatten()), target)
            self.error.append(d)
            self.times.append(self.current_time)

            if d < threshold:
                self.index += 1
        else:
            v, w = 0, 0

        self.robot.set_robot_speeds(v, w)
        self.robot.update(dt)
        self.current_time += dt

    def extract_history(self) -> tuple:
        x: list = [p[0] for p in self.history]
        y: list = [p[1] for p in self.history]
        return x, y, self.error, self.times


def save_gif(frames: list, path: Path, fps: int) -> None:
    """Write an animated GIF with Pillow (same approach as bumpy_road)."""
    if not frames:
        raise ValueError("No frames to save.")

    path = Path(path)
    duration_ms = int(1000 / fps)
    print(f"Writing {path} ({len(frames)} frames @ {fps} fps) ...")
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
    )
    print(f"Saved GIF: {path.resolve()}")


def main() -> None:
    print(f"Running with the example: {args.path}")
    waypoints = load_map(args.path)
    app: Application = Application((500, 500), "Example")

    # initialize robot and controller
    pid_ctrl = PID(0.5, 0, 0.1, 0.4, 0, 0.1)
    mpc_ctrl = MPC(5)

    pid_robot = Robot(50, 50)
    mpc_robot = Robot(50, 50)

    # initialize the pipeline
    pid = Pipeline(pid_robot, waypoints, pid_ctrl.update)
    mpc = Pipeline(
        mpc_robot, waypoints,
        lambda _, target: mpc_ctrl.update(target, mpc_robot),
    )

    frames: list = []

    while True:
        app.clean()
        app.plot(pid_robot.points, (255, 165, 0))
        app.plot(mpc_robot.points, (128, 128, 128))

        app.plot_path(waypoints, (255, 0, 0))
        app.plot_path(pid.history, (255, 165, 0), True)
        app.plot_path(mpc.history, (128, 128, 128), True)

        if args.gif:
            frames.append(app.grab_rgb())

        if (app.show() & 0xFF) == ord("q"):
            break

        pid.update(0.5)
        mpc.update(0.5)

        # When recording a GIF, stop once both robots finish the path
        if args.gif and pid.finished and mpc.finished:
            # one last frame with the completed trails
            app.clean()
            app.plot(pid_robot.points, (255, 165, 0))
            app.plot(mpc_robot.points, (128, 128, 128))
            app.plot_path(waypoints)
            app.plot_path(pid.history, (255, 165, 0), True)
            app.plot_path(mpc.history, (128, 128, 128), True)
            frames.append(app.grab_rgb())
            app.show()
            break

    if args.gif:
        save_gif(frames, Path(args.gif), args.fps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare PID and MPC path tracking (optional GIF export)."
    )
    parser.add_argument(
        "-p", "--path",
        type=str, required=True,
        help="Path to the waypoints file for the navigation example.",
    )
    parser.add_argument(
        "--gif",
        type=str, default="",
        help="Output GIF filename (Pillow). Empty string skips export.",
    )
    parser.add_argument(
        "--fps",
        type=int, default=12,
        help="Frames per second for the GIF (default: 12).",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        raise FileNotFoundError(f"{args.path} file is not found.")

    main()
