"""Contains `World` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from two_d_library.world import World as BaseWorld

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import Obstacle
from two_d_game_ai.world.grid import Grid
from two_d_game_ai.world.grid_ref import GridRef

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities.generic_entity import (
        GenericEntity,
    )


class World(BaseWorld):
    """Simulated domain.

    Square with origin at centre.

    Has a `two_d_game_ai.world.grid.Grid`.
    """

    def __init__(self, grid_size: int = 2, **kwargs: tuple[int, int]) -> None:
        super().__init__(centered_origin=True, **kwargs)
        if self.size.x != self.size.y:
            err_msg = "Size of world must be square."
            raise ValueError(err_msg)

        self.grid = Grid(size=grid_size)
        self.generic_entities: set[GenericEntity] = set()
        self.grid_resolution = self.size.x / self.grid.size
        self.is_paused = True
        logger.info(f"{self} initialized.")

    @property
    def time_step(self) -> float:
        return 1 / SIMULATION_FPS

    @property
    def bots(self) -> set[Bot]:
        """TO DO."""
        return {e for e in self.generic_entities if isinstance(e, Bot)}

    @property
    def obstacles(self) -> set[GenericEntity]:
        """TO DO."""
        return {e for e in self.generic_entities if isinstance(e, Obstacle)}

    def update_(self) -> None:
        """Only Bots currently need to be updated."""
        for e in self.generic_entities:
            if isinstance(e, Bot):
                e.update(self.time_step)

    def position_is_movement_blocked(self, position: Vector2) -> bool:
        """Return `True` if `position` is inside a movement-blocked grid cell,
        else `False`.
        """
        grid_ref = self.grid_ref_from_pos(position)
        return grid_ref in self.grid.movement_blocking_cells

    def random_position(self) -> Vector2:
        """Return random position, not movement-blocked."""
        position = self.random_position()
        if self.position_is_movement_blocked(position):
            return self.random_position()

        return position

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

        from_cell = self.grid_ref_from_pos(from_pos)
        to_cell = self.grid_ref_from_pos(to_pos)
        cell_route = self.grid.route(from_cell, to_cell)

        if not isinstance(cell_route, list):
            return None

        pos_route = [Grid.cell_centre_to_world_pos(self, cell) for cell in cell_route]
        # always use actual points (not cell centre) for end waypoints:
        pos_route[0] = from_pos
        pos_route[-1] = to_pos
        return pos_route

    def add_generic_entity(self, entity: GenericEntity) -> None:
        """Add an entity to `World`.

        Supertype's `World.add_entity` is incompatible.
        """
        entity.id = len(self.generic_entities)
        self.generic_entities.add(entity)
        entity.world = self
        if isinstance(entity, Obstacle):
            entity.add_to_grid(self.grid)

        logger.info(f"{self}: added {entity!s}.")
        if not self.position_is_in_bounds(entity.position):
            logger.warning(f"{entity!s}: outside World bounds.")

    def grid_ref_from_pos(self, pos: Vector2) -> GridRef:
        """Return the `GridRef` of the cell containing `World` position."""
        relative_pos = pos + self.origin_offset
        grid_ref = GridRef(
            int(relative_pos.x // self.grid_resolution),
            int(relative_pos.y // self.grid_resolution),
        )
        if any(
            (
                grid_ref.x < 0,
                grid_ref.y < 0,
                grid_ref.x > self.grid.size,
                grid_ref.y > self.grid.size,
            )
        ):
            err_msg = f"Can't get a `GridRef` for pos {pos} outside {self}."
            raise ValueError(err_msg)

        return grid_ref
