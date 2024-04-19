"""Generic entity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.entities.observer import Subject

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.world import World


class GenericEntity(Subject):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    pos: Vector2
        Position (World coordinates)
    world: World
    """

    def __init__(self, world: World, name: str, pos: Vector2) -> None:
        super().__init__(name)
        self.pos = pos
        self.world = world
