"""Define the Bot class."""

from pygame import Vector2


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

    """

    MAX_SPEED = 1
    DEFAULT_HEADING = Vector2(0, 0)

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

    @property
    def speed(self) -> float:
        """Return speed."""
        return self.velocity.magnitude()
