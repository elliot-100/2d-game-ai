"""Contains generic entity classes."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.world import World

_logger = logging.getLogger(__name__)


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
        log_msg = f"{self.description} initialised."
        _logger.debug(log_msg)

    def __hash__(self) -> int:
        if self.id is None:
            err_msg = f"Can't hash {self.description}: no `id`. Add to World first."
            raise ValueError(err_msg)
        return self.id

    @property
    def description(self) -> str:
        """Description of entity."""
        return f"{type(self).__name__} '{self.name}' id={self.id}"

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
