"""Package containing the `World` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.pathfinding import GridRef
from two_d_game_ai.pathfinding.grid import Grid

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities import Bot, MovementBlock


class World:
    """Simulated domain.

    Square.

    Has a `Grid`.
    """

    def __init__(
        self,
        size: int,
        grid_size: int = 2,
    ) -> None:
        self.size = size
        """`World` units per side."""
        self.grid = Grid(size=grid_size)
        """`Grid` instance."""
        self.grid_resolution = self.size / grid_size
        """Size of a `Grid` cell in `World` units."""
        self.bots: list[Bot] = []
        """All `Bot`s."""
        self.movement_blocks: list[MovementBlock] = []
        """All `MovementBlock`s."""
        self.step_counter: int = 0
        """Number of update steps taken."""
        self.is_paused: bool = True
        """Whether the `World` is paused."""

    def update(self) -> None:
        """Change all `Bot` positions over 1 simulation step."""
        for bot in self.bots:
            other_bots = [b for b in self.bots if b is not bot]
            bot.update(other_bots)
        self.step_counter += 1

    def point_is_inside_world_bounds(self, point: Vector2) -> bool:
        """Return `True` if point is inside the World bounds, else `False`.

        Not currently used.
        """
        return abs(point.x) <= self.size / 2 and abs(point.y) <= self.size / 2

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
        from_cell = GridRef.cell_from_world_pos(self, from_pos)
        to_cell = GridRef.cell_from_world_pos(self, to_pos)

        if from_cell == to_cell:  # intra-cell route is always direct
            return [to_pos]

        cell_route = self.grid.route(from_cell, to_cell)

        if not cell_route:
            return []

        pos_route = [cell.cell_centre_to_world_pos(self) for cell in cell_route]
        pos_route[-1] = (
            to_pos  # always use actual goal (not cell centre) for last waypoint
        )
        if len(pos_route) > 1:
            del pos_route[0]
        return pos_route
