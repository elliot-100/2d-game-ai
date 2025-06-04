"""Contains `ObstacleCircle` classes."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from two_d_game_ai.entities.generic_entity import GenericEntity

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.grid import Grid


@dataclass(kw_only=True, eq=False)
class Obstacle(GenericEntity, ABC):
    """Entity that blocks movement."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)

    def add_to_grid(self, grid: Grid) -> None:
        """Set relevant grid cells to untraversable."""
        grid.movement_blocking_cells.update(self.occupied_cells())


@dataclass(kw_only=True, eq=False)
class ObstacleCircle(Obstacle):
    """Circular entity that blocks movement."""

    radius: float = 1
    """Radius in `World` units."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)


@dataclass(kw_only=True, eq=False)
class ObstacleRectangle(Obstacle):
    """Rectangular entity that blocks movement."""

    size: tuple[float, float] = 2, 2
    """Size in `World` units."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)
