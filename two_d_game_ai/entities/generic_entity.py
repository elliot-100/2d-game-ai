"""Contains generic entity classes."""

from __future__ import annotations

from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from loguru import logger
from pygame import Vector2

from two_d_game_ai.geometry import point_in_or_on_circle, point_in_or_on_rect
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.grid_ref import GridRef
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
        return f"{type(self).__name__}('{self.name}')"

    @property
    def is_inside_world_bounds(self) -> bool:
        """Return `True` if entity is inside the World bounds, else `False`."""
        if self.world is None:
            err_msg = f"Can't check {self!s} inside bounds. Add to World first."
            raise ValueError(err_msg)
        return self.world.location_is_inside_world_bounds(self.position)

    def occupied_cells(self) -> set[GridRef]:
        """TODO."""
        if not self.world:
            err_msg = "UNHANDLED. Add to World first."
            raise ValueError(err_msg)

        occupied_cells = set()
        if hasattr(self, "radius"):
            for cell in self.world.grid.cells:
                cell_centre = Grid.cell_centre_to_world_pos(self.world, cell)
                if point_in_or_on_circle(
                    point=cell_centre,
                    circle_centre=self.position,
                    circle_radius=self.radius,
                ):
                    occupied_cells.add(cell)

        elif hasattr(self, "size"):
            for cell in self.world.grid.cells:
                cell_centre = Grid.cell_centre_to_world_pos(self.world, cell)
                if point_in_or_on_rect(
                    point=cell_centre,
                    rect_min=self.position,
                    rect_size=Vector2(self.size),
                ):
                    occupied_cells.add(cell)

        return occupied_cells
