"""Contains `GenericEntity` class."""

from __future__ import annotations

import logging
from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.world import World

_logger = logging.getLogger(__name__)


@dataclass(kw_only=True, eq=False)
class GenericEntity(ABC):
    """Generic circular entity."""

    id: None | int = field(init=False, default=None)
    """Unique identifier within World. `None` until added to `World`."""
    world: None | World = field(init=False, default=None)
    """Reference to `World` object. `None` until added to `World`."""
    position_from_sequence: InitVar[Sequence[float]]
    """`World` coordinates."""
    position: Vector2 = field(init=False)
    """Position in `World` coordinates, as `Vector2`."""
    radius: float = 0
    """Radius in `World` units. Default is 0."""
    name: str = "GenericEntity"
    """May be shown in UI and logging."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        self.position = Vector2(position_from_sequence)
        log_msg = f"{type(self).__name__} '{self.name}' initialised."
        _logger.debug(log_msg)

    def __hash__(self) -> int:
        if self.id is None:
            # TypeGuard
            err_msg = "Entity has no `id` to hash. Add to World first."
            raise TypeError(err_msg)
        return self.id
