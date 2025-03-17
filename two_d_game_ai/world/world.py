"""Module containing `World` class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities.bot import Bot
    from two_d_game_ai.entities.movement_block import MovementBlock


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
    entities: set[Any] = field(default_factory=set)
    """All entities."""
    bots: set[Bot] = field(default_factory=set)
    """All `Bot`s."""
    movement_blocks: list[MovementBlock] = field(default_factory=list)
    """All `MovementBlock`s."""
    step_counter: int = 0
    """Number of update steps taken."""
    is_paused: bool = True
    """Whether the `World` is paused."""

    def __post_init__(
        self,
    ) -> None:
        self.grid = Grid(size=self.grid_size)
        self.grid_resolution = self.size / self.grid_size

    def update(self) -> None:
        """Change all `Bot` positions over 1 simulation step."""
        for bot in self.bots:
            bot.update({b for b in self.bots if b is not bot})
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
        from_cell = Grid.cell_from_world_pos(self, from_pos)
        to_cell = Grid.cell_from_world_pos(self, to_pos)

        if from_cell == to_cell:  # intra-cell route is always direct
            return [to_pos]

        cell_route = self.grid.route(from_cell, to_cell)

        if not cell_route:
            return []

        pos_route = [Grid.cell_centre_to_world_pos(cell, self) for cell in cell_route]
        pos_route[-1] = to_pos
        # always use actual goal (not cell centre) for last waypoint
        if len(pos_route) > 1:
            del pos_route[0]
        return pos_route
