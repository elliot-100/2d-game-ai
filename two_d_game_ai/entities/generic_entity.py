"""Package containing `GenericEntity` class."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from two_d_game_ai import Vector2
from two_d_game_ai.entities.observer_pattern import _Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class GenericEntity(_Subject, ABC):
    """Generic circular entity."""

    def __init__(self, world: World, name: str, pos: tuple[float, float]) -> None:
        super().__init__(name)
        self.world = world
        self.pos = pos
        """Position in `World` coordinates."""
        self.pos_v = Vector2(pos)
        """Position in `World` coordinates, as `Vector2`."""
