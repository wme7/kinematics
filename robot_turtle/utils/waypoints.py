from typing import Optional


class WaypointHandler(object):
    def __init__(self) -> None:
        self._path: list[tuple[int, int]] = []
        self.index: int = 0

    def add_waypoint(
        self,
        button: int,
        x: int,
        y: int,
        flags: Optional[int] = None,
        param: Optional[int] = None,
    ) -> None:
        """Adds or removes waypoints based on mouse button presses.

        Left click (button 1) appends a waypoint; right click (button 3) pops
        the last waypoint if any exist.
        """
        _ = flags, param
        if button == 1:
            self._path.append((x, y))
        if button == 3 and self._path:
            self._path.pop()

    @property
    def path(self) -> list[tuple[int, int]]:
        return self._path
