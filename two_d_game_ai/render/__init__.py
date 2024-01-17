"""Package for rendering the model using Pygame."""
from pygame import Vector2

from two_d_game_ai.world import World

BACKGROUND_COLOR = GREY_80 = (51, 51, 51)
FOREGROUND_COLOR = RED = (255, 0, 0)

CAPTION = "2dGameAI"
FONT_SIZE = 24


def to_display(world: World, world_pos: Vector2) -> Vector2:
    """Convert world coordinates to window coordinates.

    Parameters
    ----------
    world: World

    world_pos
        World coordinates

    Returns
    -------
    Vector2
        Window coordinates, with origin at centre
    """
    display_pos = (world_pos[0], -world_pos[1])
    offset = Vector2(world.radius, world.radius)
    return display_pos + offset
