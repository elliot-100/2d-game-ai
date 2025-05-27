"""Contains `ObstacleCircle` classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai.entities.generic_entities import (
    GenericEntity,
    GenericEntityCircle,
    GenericEntityRectangle,
)
from two_d_game_ai.geometry import point_in_or_on_circle, point_in_or_on_rect
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence


def is_obstacle(obj: GenericEntity) -> bool:
    """Check if entity is an `Obstacle`."""
    return isinstance(obj, ObstacleCircle | ObstacleRectangle)


@dataclass(kw_only=True, eq=False)
class ObstacleCircle(GenericEntityCircle):
    """Circular entity that blocks movement."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)

    def add_to_grid(self) -> None:
        """Set relevant grid cells to untraversable."""
        if not self.world:
            err_msg = f"Can't add {self!s} to grid. Add to World first."
            raise ValueError(err_msg)

        for cell in self.world.grid.cells:
            cell_centre = Grid.cell_centre_to_world_pos(self.world, cell)
            if point_in_or_on_circle(
                point=cell_centre,
                circle_centre=self.position,
                circle_radius=self.radius,
            ):
                self.world.grid.movement_blocking_cells.add(cell)


@dataclass(kw_only=True, eq=False)
class ObstacleRectangle(GenericEntityRectangle):
    """Rectangular entity that blocks movement."""

    def __post_init__(self, position_from_sequence: Sequence[float]) -> None:
        super().__post_init__(position_from_sequence)

    def add_to_grid(self) -> None:
        """Set relevant grid cells."""
        if not self.world:
            err_msg = f"Can't add {self!s} to grid. Add to World first."
            raise ValueError(err_msg)

        for cell in self.world.grid.cells:
            cell_centre = Grid.cell_centre_to_world_pos(self.world, cell)
            if point_in_or_on_rect(
                point=cell_centre,
                rect_min=self.position,
                rect_size=Vector2(self.size),
            ):
                self.world.grid.movement_blocking_cells.add(cell)
