import pygame
import numpy as np

from typing import Callable, Optional

color_tuple = tuple[int, int, int]


class Application(object):
    def __init__(
        self,
        window_size: tuple[int, int],
        window_name: str,
        callback: Optional[Callable] = None,
    ) -> None:
        if not pygame.get_init():
            pygame.init()

        self.w, self.h = window_size
        self.name: str = window_name
        self._callback = callback
        self._clock = pygame.time.Clock()

        pygame.display.set_caption(self.name)
        self.canvas: pygame.Surface = pygame.display.set_mode((self.w, self.h))
        self.color: color_tuple = (255, 255, 255)

    def clean(self) -> None:
        self.canvas.fill(self.color)

    def plot(
        self,
        points: np.ndarray,
        color: color_tuple = (255, 0, 0),
        thickness: int = 2,
    ) -> None:
        for i in range(len(points) - 1):
            pygame.draw.line(
                self.canvas,
                color,
                (int(points[i, 0]), int(points[i, 1])),
                (int(points[i + 1, 0]), int(points[i + 1, 1])),
                thickness,
            )

        pygame.draw.line(
            self.canvas,
            color,
            (int(points[0, 0]), int(points[0, 1])),
            (int(points[-1, 0]), int(points[-1, 1])),
            thickness,
        )

    def plot_path(
        self,
        path: list[tuple[int, int]],
        color: color_tuple = (128, 128, 128),
        dotted: bool = False,
    ) -> None:
        if not path:
            return

        if dotted:
            for i, point in enumerate(path[:-1]):
                if not (i % 3):
                    self._plot_circle(point, color, 2)
            return

        for p1, p2 in zip(path[:-1], path[1:]):
            pygame.draw.line(self.canvas, color, p1, p2, 1)
        self._plot_circle(path[-1], color)

    def label(
        self,
        text: str,
        color: color_tuple = (255, 0, 0),
        thickness: int = 2,
        font_size: float = 1,
        org: tuple[int, int] = (100, 50),
    ) -> None:
        size = max(12, int(24 * font_size))
        font = pygame.font.SysFont("dejavusans", size)
        # thickness is unused; kept for API compatibility with the old OpenCV version
        _ = thickness
        surface = font.render(text, True, color)
        self.canvas.blit(surface, org)

    def grab_rgb(self):
        """Return a Pillow ``Image`` of the current canvas (RGB)."""
        from PIL import Image

        raw = pygame.image.tobytes(self.canvas, "RGB")
        return Image.frombytes("RGB", (self.w, self.h), raw)

    def show(self) -> int:
        key_code = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                key_code = event.key
            if event.type == pygame.MOUSEBUTTONDOWN and self._callback is not None:
                self._callback(event.button, event.pos[0], event.pos[1])

        pygame.display.flip()
        self._clock.tick(33)
        return key_code

    def _plot_circle(
        self,
        point: tuple[int, int],
        color: color_tuple,
        radius: int = 3,
    ) -> None:
        pygame.draw.circle(self.canvas, color, point, radius)
