"""Package containing `MovementBlock` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.world.grid import Grid

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MovementBlock(GenericEntity):
    """Circular entity that blocks movement."""

    def __post_init__(self, position_from_tuple: tuple[float, float]) -> None:
        super().__post_init__(position_from_tuple)
        for cell in self.world.grid.cells:
            cell_centre = Grid.cell_centre_to_world_pos(cell, self.world)
            if point_in_or_on_circle(
                cell_centre,
                self.position,
                self.radius,
            ):
                self.world.grid.untraversable_cells.add(cell)

        log_msg = f"MovementBlock '{self.name}' created."
        logger.info(log_msg)

    def __hash__(self) -> int:
        return super().__hash__()
