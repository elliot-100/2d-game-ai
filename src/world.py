"""Define the World class."""

from __future__ import annotations

from pygame import Vector2

from src.bot import Bot


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
        for b in self.bots.values():
            b.update()
        self.step_counter += 1
