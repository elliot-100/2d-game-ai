"""Define the Bot class."""

from __future__ import annotations

from pygame import Vector2

from src.maths import relative_bearing_degrees


class Bot:
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    name: str
        Name
    pos: Vector2
        Position
    velocity: Vector2
        Velocity
    heading: Vector2
        Heading
    """

    MAX_SPEED = 1
    INITIAL_HEADING = Vector2(0, 1)
    VISION_CONE_ANGLE = 90  # degrees

    def __init__(self, name: str, pos: Vector2) -> None:
        """Initialise the instance.

        name: str
            Name
        pos: Vector2
            Position

        """
        self.name = name
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.heading = Bot.INITIAL_HEADING

    @property
    def speed(self) -> float:
        """Return speed."""
        return self.velocity.magnitude()

    def can_see(self, point: Vector2) -> bool:
        """Is the point within the Bot's vision cone?."""
        relative_bearing_to_point = relative_bearing_degrees(self.heading, point)
        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2

    def move(self) -> None:
        """Change position over 1 simulation step."""
        self.pos += self.velocity
