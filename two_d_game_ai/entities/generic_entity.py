"""Generic entity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai import Vector2
from two_d_game_ai.entities.observer import Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class GenericEntity(Subject):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    name: str
    pos: tuple[float, float] | None
        Position (World coordinates)
    pos_v: Vector2
        Position (World coordinates)
    world: World
    """

    def __init__(self, world: World, name: str, pos: tuple[float, float]) -> None:
        super().__init__(name)
        self.pos = pos
        self.pos_v = Vector2(pos)
        self.world = world
