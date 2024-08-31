"""Package containing `MovementBlock` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from two_d_game_ai.entities.generic_entity import GenericEntity

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
        super().__init__(world, name, pos)
        self.radius = radius
        self.world.movement_blocks.append(self)
        log_msg = f"MovementBlock '{self.name}' created."
        logging.info(log_msg)

    def update(self) -> None:
        """No update needed."""
