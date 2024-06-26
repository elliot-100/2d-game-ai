"""MovementBlock class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from two_d_game_ai.entities.generic_entity import _GenericEntity

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class MovementBlock(_GenericEntity):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    name: str
    collision_radius: float
        Radius for collision detection
    pos: tuple[float, float]
        Position (World coordinates)
    pos_v: Vector2
        Position (World coordinates)
    world: World

    """

    def __init__(
        self, world: World, name: str, pos: tuple[float, float], collision_radius: float
    ) -> None:
        super().__init__(world, name, pos)
        self.collision_radius = collision_radius
        self.world.movement_blocks.append(self)
        log_msg = f"MovementBlock '{self.name}' created."
        logging.info(log_msg)

    def update(self) -> None:
        """No update needed."""
