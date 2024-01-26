"""World class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Vector2

    from two_d_game_ai.bot import Bot


class World:
    """Simulated domain.

    Assumed circular.

    Attributes
    ----------
    radius: float
        Radius
    bots: list[Bot]
        All bots in the World.
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius
        self.bots: list[Bot] = []
        self.step_counter = 0

    def update(self) -> None:
        """Change all Bot positions over 1 simulation step."""
        for bot in self.bots:
            other_bots = [b for b in self.bots if b is not bot]
            bot.update(other_bots)
        self.step_counter += 1

    def point_is_outside_world_bounds(self, point: Vector2) -> bool:
        """Return True if point is inside the World bounds."""
        return point.magnitude_squared() >= self.radius**2
