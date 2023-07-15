"""Define the Bot class."""

from __future__ import annotations

from pygame import Vector2

from src.maths import relative_bearing_degrees


class Bot:
    """Simulated entity.

    Assumed circular.

    Class attributes
    ----------------
    MAX_SPEED: int

    Attributes
    ----------
    name: str
        Name
    pos: Vector2
        Position
    speed: float
        Speed
    velocity: Vector2
        Velocity
    heading: Vector2
        Heading
    vision_cone_angle: float
        In degrees
    """

    MAX_SPEED = 1
    DEFAULT_HEADING = Vector2(0, 1)
    DEFAULT_VISION_CONE_ANGLE_DEGREES = 90

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
        self.heading = Bot.DEFAULT_HEADING
        self.vision_cone_angle = Bot.DEFAULT_VISION_CONE_ANGLE_DEGREES

    @property
    def speed(self) -> float:
        """Return speed."""
        return self.velocity.magnitude()

    def can_see(self, point: Vector2) -> bool:
        """Is the point within the Bot's vision cone?."""
        relative_bearing_to_point = relative_bearing_degrees(self.heading, point)
        return abs(relative_bearing_to_point) <= self.vision_cone_angle / 2
