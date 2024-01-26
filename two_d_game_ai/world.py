"""Package containing the `World` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.entities import Bot, MovementBlock


class World:
    """Simulated domain.

    Square.
    """

    def __init__(self, size: int) -> None:
        self.size = size
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

    def point_is_outside_world_bounds(self, point: Vector2) -> bool:
        """Return True if point is inside the World bounds."""
        return point.magnitude_squared() >= self.radius**2
