"""Package for rendering the model using Pygame."""
from pygame import Vector2

from two_d_game_ai.world import World

BACKGROUND_COLOR = GREY_80 = (51, 51, 51)
FOREGROUND_COLOR = RED = (255, 0, 0)

CAPTION = "2dGameAI"
FONT_SIZE = 24


def to_display(world: World, world_pos: Vector2, scale_factor: float) -> Vector2:
    """Convert world coordinates to display window coordinates.

    Parameters
    ----------
    world: World
    world_pos
        World coordinates
    scale_factor

    Returns
    -------
    Vector2
        Display window coordinates.
        Origin is at centre, positive y upwards (opposite to Pygame, etc).
    """
    display_pos = scale_factor * Vector2(world_pos.x, -world_pos.y)
    offset = scale_factor * Vector2(world.radius, world.radius)
    return display_pos + offset
