"""Contains generic entity classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from loguru import logger
from pygame import Vector2

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.world import World


@dataclass(kw_only=True, eq=False)
class GenericEntity(ABC):
    """Generic entity."""

    id: None | int = field(init=False, default=None)
    """Unique identifier within World. `None` until added to `World`."""
    world: None | World = field(init=False, default=None)
    """Reference to `World` object. `None` until added to `World`."""
    position_from_sequence: InitVar[Sequence[float]]
    """`World` coordinates."""
    position: Vector2 = field(init=False)
    """Position in `World` coordinates, as `Vector2`."""
    name: str = "ANON ENTITY"
    """May be shown in UI and logging."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        self.position = Vector2(position_from_sequence)
        if self.world and not self.is_inside_world_bounds:
            logger.warning(f"{self!s}: outside World bounds.")

    def __hash__(self) -> int:
        if self.id is None:
            err_msg = f"Can't hash {self!s}: no `id`. Add to World first."
            raise ValueError(err_msg)
        return self.id

    def __str__(self) -> str:
        """Human-readable description."""
        return f"{type(self).__name__} '{self.name}', id={self.id}"

    @property
    def is_inside_world_bounds(self) -> bool:
        """Return `True` if entity is inside the World bounds, else `False`."""
        if self.world is None:
            err_msg = f"Can't check {self!s} inside bounds. Add to World first."
            raise ValueError(err_msg)
        return self.world.location_is_inside_world_bounds(self.position)

    @abstractmethod
    def add_to_grid(self) -> None:
        """Not implemented."""


@dataclass(kw_only=True, eq=False)
class GenericEntityCircle(GenericEntity, ABC):
    """Generic circular entity."""

    radius: float = 1
    """Radius in `World` units. Default is 1."""


@dataclass(kw_only=True, eq=False)
class GenericEntityRectangle(GenericEntity, ABC):
    """Generic rectangular entity."""

    size: tuple[float, float] = 2, 2
    """Size in `World` units. Default is 2, 2."""
