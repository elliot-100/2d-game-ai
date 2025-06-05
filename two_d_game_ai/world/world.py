"""Contains `World` class."""

from __future__ import annotations

import random
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from loguru import logger
from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import Obstacle
from two_d_game_ai.geometry import point_in_or_on_rect
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from two_d_game_ai.entities.generic_entity import (
        GenericEntity,
    )


@dataclass
class World:
    """Simulated domain.

    Square with origin at centre.

    Has a `two_d_game_ai.world.grid.Grid`.
    """

    size: int
    """`World` units per side."""
    grid_size: InitVar[int] = 2

    magnitude: float = field(init=False)
    """Half of `World` size."""
    grid: Grid = field(init=False)
    """`Grid` instance."""
    grid_resolution: float = field(init=False)
    """Size of a `Grid` cell in `World` units."""
    grid_offset: Vector2 = field(init=False)
    """Origin of `Grid` in `World` coordinates."""
    cell_size: float = field(init=False)
    """Size of a `Grid` cell in `World` units."""
    entities: set[GenericEntity] = field(init=False, default_factory=set)
    """All entities."""
    step_counter: int = field(init=False)
    """Number of update steps taken."""
    is_paused: bool = field(init=False)
    """Whether the `World` is paused."""

    def __post_init__(self, grid_size: int) -> None:
        self.magnitude = self.size / 2
        self.grid = Grid(size=grid_size)
        self.grid_resolution = self.size / self.grid.size
        self.grid_offset = -Vector2(self.magnitude, self.magnitude)
        self.step_counter = 0
        self.is_paused = True
        logger.info(f"{self!s}(size={self.size}) initialized.")

    def __str__(self) -> str:
        """Human-readable description."""
        return f"{type(self).__name__}"

    @property
    def bots(self) -> set[Bot]:
        """TO DO."""
        return {e for e in self.entities if isinstance(e, Bot)}

    @property
    def obstacles(self) -> set[GenericEntity]:
        """TO DO."""
        return {e for e in self.entities if isinstance(e, Obstacle)}

    def update(self) -> None:
        """Only Bots currently need to be updated."""
        for e in self.entities:
            if isinstance(e, Bot):
                e.update()
        self.step_counter += 1

    def location_is_inside_world_bounds(self, location: Vector2) -> bool:
        """Return `True` if point is inside the World bounds, else `False`."""
        return point_in_or_on_rect(
            point=location,
            rect_min=Vector2(-self.magnitude, -self.magnitude),
            rect_size=Vector2(self.size, self.size),
        )

    def location_is_movement_blocked(self, location: Vector2) -> bool:
        """Return `True` if `location` is inside a movement-blocked grid cell,
        else `False`.
        """
        grid_ref = self.grid.grid_ref_from_world_pos(self, location)
        return grid_ref in self.grid.movement_blocking_cells

    def random_location(self) -> Vector2:
        """Return random location, not movement-blocked."""
        location = Vector2(
            random.uniform(-self.magnitude, self.magnitude),
            random.uniform(-self.magnitude, self.magnitude),
        )
        if self.location_is_movement_blocked(location):
            return self.random_location()

        return location

    def route(
        self,
        *,
        from_pos: Vector2,
        to_pos: Vector2,
    ) -> list[Vector2] | None:
        """Determine a route between two locations.

        Parameters
        ----------
        from_pos
            A point in `World` coordinates.
        to_pos
            A point in `World` coordinates.

        Returns
        -------
        list[Vector2]
            Points on the path, including `to_pos` itself.
            Empty if no route was found.
        """
        if not self.grid.movement_blocking_cells:
            return [to_pos]

        from_cell = Grid.grid_ref_from_world_pos(self, from_pos)
        to_cell = Grid.grid_ref_from_world_pos(self, to_pos)
        cell_route = self.grid.route(from_cell, to_cell)

        if not isinstance(cell_route, list):
            return None

        pos_route = [Grid.cell_centre_to_world_pos(self, cell) for cell in cell_route]
        # always use actual points (not cell centre) for end waypoints:
        pos_route[0] = from_pos
        pos_route[-1] = to_pos
        return pos_route

    def add_entity(self, entity: GenericEntity) -> None:
        """Add an entity to `World`."""
        entity.id = len(self.entities)
        self.entities.add(entity)
        entity.world = self
        if isinstance(entity, Obstacle):
            entity.add_to_grid(self.grid)

        logger.info(f"{self}: added {entity!s}.")
        if not self.location_is_inside_world_bounds(entity.position):
            logger.warning(f"{entity!s}: outside World bounds.")
