"""Contains `MovementBlock` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(kw_only=True, eq=False)
class MovementBlock(GenericEntity):
    """Circular entity that blocks movement."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)

    def add_to_grid(self) -> None:
        """Set obscured grid cells to untraversable."""
        if self.world is None:
            # TypeGuard
            err_msg = "MovementBlock needs to be added to World first."
            raise TypeError(err_msg)
        for cell in self.world.grid.cells:
            cell_centre = Grid.cell_centre_to_world_pos(cell, self.world)
            if point_in_or_on_circle(
                cell_centre,
                self.position,
                self.radius,
            ):
                self.world.grid.untraversable_cells.add(cell)
