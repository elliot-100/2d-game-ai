"""Define the World class."""

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
    bots: dict[str, Bot]
        All bots in the World.
        Key is Bot.name
        Value is Bot instance.
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius
        self.bots: dict[str, Bot] = {}
        self.step_counter = 0

    def add_bot(self, name: str, pos: Vector2) -> None:
        """Add a Bot to the World."""
        self.bots[name] = Bot(name, pos)

    def update(self) -> None:
        """Change all Bot positions over 1 simulation step."""
        for bot in self.bots.values():
            other_bots = [b for b in self.bots.values() if b is not bot]
            bot.update(other_bots)
        self.step_counter += 1
