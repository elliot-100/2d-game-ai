"""Package containing `GenericEntity` class."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field

from pygame import Vector2

from two_d_game_ai.entities.observer_pattern import Subject


@dataclass(kw_only=True)
class GenericEntity(Subject, ABC):
    """Generic circular entity."""

    position: tuple[float, float]
    # TODO: should be InitVar
    """`World` coordinates."""
    pos: Vector2 = field(init=False)
    """Position in `World` coordinates, as `Vector2`."""
    radius: float = 0
    """Radius in `World` units. Default is 0."""

    def __post_init__(self) -> None:
        Subject.__post_init__(self)
        self.pos = Vector2(self.position)

    def __hash__(self) -> int:
        return Subject.__hash__(self)
