"""Define the World class."""

from pygame import Vector2

from src.bot import Bot


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

    def add_bot(self, pos: Vector2) -> None:
        """Add a Bot to the World."""
        self.bots.append(Bot(pos))
