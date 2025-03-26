"""Contains `World` class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities.generic_entity import GenericEntity


@dataclass
class World:
    """Simulated domain.

    Square.

    Has a `two_d_game_ai.world.grid.Grid`.
    """

    size: int
    """`World` units per side."""
    grid_size: int = 2
    # TODO: should be InitVar and/or derived from Grid classvar
    grid_resolution: float = field(init=False)
    """Size of a `Grid` cell in `World` units."""
    grid: Grid = field(init=False)
    """`Grid` instance."""
    entities: set[GenericEntity] = field(init=False, default_factory=set)
    """All entities."""
    step_counter: int = field(init=False)
    """Number of update steps taken."""
    is_paused: bool = field(init=False)
    """Whether the `World` is paused."""

    def __post_init__(
        self,
    ) -> None:
        self.grid = Grid(size=self.grid_size)
        self.grid_resolution = self.size / self.grid_size
        self.step_counter = 0
        self.is_paused = True

    @property
    def magnitude(self) -> float:
        """TO DO."""
        return self.size / 2

    @property
    def bots(self) -> set[Bot]:
        """TO DO."""
        return {e for e in self.entities if isinstance(e, Bot)}

    @property
    def movement_blocks(self) -> set[MovementBlock]:
        """TO DO."""
        return {e for e in self.entities if isinstance(e, MovementBlock)}

    def update(self) -> None:
        """Only Bots currebtly need to be updated."""
        for e in self.entities:
            if isinstance(e, Bot):
                e.update()
        self.step_counter += 1

    def point_is_inside_world_bounds(self, point: Vector2) -> bool:
        """Return `True` if point is inside the World bounds, else `False`.

        Not currently used.
        """
        return abs(point.x) <= self.magnitude and abs(point.y) <= self.magnitude

    def route(
        self,
        from_pos: Vector2,
        to_pos: Vector2,
    ) -> list[Vector2]:
        """Return route.

        Uses uniform cost search, a variation of Dijkstra's algorithm.
        Delegates to `Grid.route`.
        Intermediate points are cell centres.

        Returns
        -------
        list[Vector2]
            Points on the path, including `to_pos` itself.
            Empty if no path found.
        """
        from_cell = Grid.cell_from_world_pos(self, from_pos)
        to_cell = Grid.cell_from_world_pos(self, to_pos)

        if from_cell == to_cell:  # intra-cell route is always direct
            return [to_pos]

        cell_route = self.grid.route(from_cell, to_cell)

        if not cell_route:
            return []

        pos_route = [Grid.cell_centre_to_world_pos(cell, self) for cell in cell_route]
        # always use actual points (not cell centre) for end waypoints:
        pos_route[0] = from_pos
        pos_route[-1] = to_pos
        return pos_route
