"""Contains `GenericEntity` class."""

from __future__ import annotations

from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai.entities.subject import Subject

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(kw_only=True)
class GenericEntity(Subject, ABC):
    """Generic circular entity."""

    position_from_sequence: InitVar[Sequence[float]]
    """`World` coordinates."""
    position: Vector2 = field(init=False)
    """Position in `World` coordinates, as `Vector2`."""
    radius: float = 0
    """Radius in `World` units. Default is 0."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        Subject.__post_init__(self)
        self.world.entities.add(self)
        self.position = Vector2(position_from_sequence)

    def __hash__(self) -> int:
        return Subject.__hash__(self)
