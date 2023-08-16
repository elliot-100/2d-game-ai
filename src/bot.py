"""Define the Bot class."""

from __future__ import annotations

from pygame import Vector2

from src import SIMULATION_STEP_INTERVAL_S
from src.maths import relative_bearing_degrees


class Bot:
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    destination: Vector2
        Destination
    name: str
        Name
    pos: Vector2
        Position
    velocity: Vector2
        Velocity (units per simulated second)
    heading: Vector2
        Heading
    """

    MAX_SPEED = 60  # units per simulated second
    INITIAL_HEADING = Vector2(0, 1)
    VISION_CONE_ANGLE = 90  # degrees

    def __init__(self, name: str, pos: Vector2) -> None:
        """Initialise the instance.

        name: str
            Name
        pos: Vector2
            Position

        """
        self.destination: None | Vector2 = None
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
        if self.destination:
            displacement = self.destination - self.pos
            displacement.scale_to_length(Bot.MAX_SPEED)
            self.velocity = displacement
        self.pos += self.velocity * SIMULATION_STEP_INTERVAL_S
