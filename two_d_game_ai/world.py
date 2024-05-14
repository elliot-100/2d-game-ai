"""World class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from two_d_game_ai.entities import Bot


class World:
    """Simulated rectangular domain.

    Attributes
    ----------
    x_dimension: float
    y_dimension: float
    bots: list[Bot]
        All bots in the World.
    step_counter: int
        Number of update steps taken.
    is_paused: bool
        Whether the World is paused.
    """

    def __init__(self, x_dimension: float, y_dimension: float) -> None:
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.bots: list[Bot] = []
        self.step_counter = 0
        self.is_paused: bool = True

    def update(self) -> None:
        """Change all Bot positions over 1 simulation step."""
        for bot in self.bots:
            other_bots = [b for b in self.bots if b is not bot]
            bot.update(other_bots)
        self.step_counter += 1
