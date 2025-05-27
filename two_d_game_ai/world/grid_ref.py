"""Contains `GridRef` class."""

from __future__ import annotations

from dataclasses import dataclass

from pygame import Vector2


@dataclass(frozen=True)
class GridRef:
    """Grid reference class.

    NB: Not a `Grid` cell class.
    """

    x: int
    """x coordinate."""
    y: int
    """y coordinate."""

    def __add__(self, other: GridRef) -> GridRef:
        return GridRef(self.x + other.x, self.y + other.y)

    def __sub__(self, other: GridRef) -> GridRef:
        return GridRef(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Vector2:
        return Vector2(self.x * other, self.y * other)
