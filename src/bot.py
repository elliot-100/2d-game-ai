from pygame import Vector2


class Bot:
    def __init__(self, pos: Vector2, radius: float) -> None:
        self.pos = pos
        self.radius = radius
