"""Module containing `GridRef` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from two_d_game_ai.world.world import World


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

    def cell_centre_to_world_pos(self, world: World) -> Vector2:
        """Return the `World` position of the centre of the cell."""
        return self._cell_to_world_pos(world) + Vector2(world.grid_resolution / 2)

    def _cell_to_world_pos(self, world: World) -> Vector2:
        """Return the `World` reference position of the cell, i.e. its min X, Y
        corner.
        """
        return Vector2(
            self.x * world.grid_resolution,
            self.y * world.grid_resolution,
        )

    @staticmethod
    def cell_from_world_pos(world: World, pos: Vector2) -> GridRef:
        """Return the `GridRef` of the cell containing `World` position."""
        return GridRef(
            int(pos.x // world.grid_resolution), int(pos.y // world.grid_resolution)
        )
