"""Package containing the `World` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.pathfinding.grid import Grid

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities import Bot, MovementBlock


class World:
    """Simulated domain.

    Square.
    """

    def __init__(
        self,
        size: int,
        grid_size: int = 2,
    ) -> None:
        self.size = size
        self.grid = Grid(size=grid_size)
        """`Grid` instance."""
        self.grid_cell_size = self.size / grid_size
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
        """Return `True` if point is inside the World bounds, else `False`."""
        return abs(point.x) <= self.size / 2 and abs(point.y) <= self.size / 2
