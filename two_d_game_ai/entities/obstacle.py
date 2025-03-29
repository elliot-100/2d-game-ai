"""Contains `Obstacle` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(kw_only=True, eq=False)
class Obstacle(GenericEntity):
    """Circular entity that blocks movement, vision, or both."""

    blocks_vision: bool = True
    blocks_movement: bool = True

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)

        blocked_cells = set()
        for cell in self.world.grid.cells:
            cell_centre = Grid.cell_centre_to_world_pos(cell, self.world)
            if point_in_or_on_circle(
                cell_centre,
                self.position,
                self.radius,
            ):
                blocked_cells.add(cell)

        if self.blocks_movement:
            self.world.grid.movement_blocking_cells.update(blocked_cells)
        if self.blocks_vision:
            self.world.grid.vision_blocking_cells.update(blocked_cells)
