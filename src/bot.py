from pygame import Vector2


class Bot:
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------

    pos: Vector2
        Position
    radius: float
        Radius

    """

    def __init__(self, pos: Vector2, radius: float) -> None:
        self.pos = pos
        self.radius = radius
