"""World class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from two_d_game_ai.entities.bot import Bot


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
        self.is_paused: bool = True

    def update(self) -> None:
        """Change all Bot positions over 1 simulation step."""
        for bot in self.bots:
            other_bots = [b for b in self.bots if b is not bot]
            bot.update(other_bots)
        self.step_counter += 1
