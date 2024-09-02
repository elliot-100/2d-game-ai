"""Module containing `GridRef` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from two_d_game_ai import Vector2

if TYPE_CHECKING:
    from two_d_game_ai.world import World


@dataclass(frozen=True)  # therefore hashable
class GridRef:
    """Grid reference class."""

    x: int
    y: int

    def __add__(self, other: GridRef) -> GridRef:
        return GridRef(self.x + other.x, self.y + other.y)

    @property
    def as_tuple(self) -> tuple[int, int]:
        """Get simple tuple representation for output."""
        return self.x, self.y

    def cell_to_pos(self, world: World) -> Vector2:
        """Return the world pos of the referenced cell, i.e. its min x, y corner."""
        return Vector2(
            self.x * world.grid_cell_size,
            self.y * world.grid_cell_size,
        )

    def cell_centre_to_pos(self, world: World) -> Vector2:
        """Return the world pos of the centre of the referenced cell."""
        return self.cell_to_pos(world) + Vector2(world.grid_cell_size / 2)

    @staticmethod
    def cell_from_pos(world: World, pos: Vector2) -> GridRef:
        """Return the `GridRef` of the cell containing `pos`."""
        return GridRef(
            int(pos.x // world.grid_cell_size), int(pos.y // world.grid_cell_size)
        )
