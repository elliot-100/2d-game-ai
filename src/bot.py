"""Define the Bot class."""

from pygame import Vector2


class Bot:
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    pos: Vector2
        Position
    """

    def __init__(self, pos: Vector2) -> None:
        self.pos = pos
