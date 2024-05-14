"""Generic entity class."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from two_d_game_ai import Vector2
from two_d_game_ai.entities.observer_pattern import _Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class _GenericEntity(_Subject, ABC):
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
        self.world = world
        self.pos = pos
        self.pos_v = Vector2(pos)
