"""Package containing `MovementBlock` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import point_in_or_on_circle

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class MovementBlock(GenericEntity):
    """Circular entity that blocks movement."""

    def __init__(
        self,
        world: World,
        name: str,
        pos: tuple[float, float],
        radius: float,
    ) -> None:
        super().__init__(world, name, pos, radius)

        for cell in self.world.grid.cells:
            if point_in_or_on_circle(
                cell.cell_centre_to_pos(self.world), Vector2(pos), radius
            ):
                world.grid.untraversable_cells.add(cell)

        self.world.movement_blocks.append(self)
        log_msg = f"MovementBlock '{self.name}' created."
        logging.info(log_msg)
