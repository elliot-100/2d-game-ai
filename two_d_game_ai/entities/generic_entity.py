"""Package containing `GenericEntity` class."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai.entities.observer_pattern import _Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class GenericEntity(_Subject, ABC):
    """Generic circular entity."""

    def __init__(
        self, world: World, name: str, position: tuple[float, float], radius: float = 0
    ) -> None:
        super().__init__(name)
        self.world = world
        """Reference to `World` object."""
        self.pos = Vector2(position)
        """Position in `World` coordinates, as `Vector2`."""
        self.radius = radius
        """Radius in `World` units. Default is 0."""
