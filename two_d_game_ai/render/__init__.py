"""Package for rendering the model using Pygame."""

from math import radians

from pygame import Vector2

from two_d_game_ai.world import World


def to_display(world: World, world_pos: Vector2, scale_factor: float) -> Vector2:
    """Scale and offset world coordinates to display window coordinates.

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


def to_display_angle_rad(bearing_deg: float) -> float:
    """Convert bearing (degrees) to Pygame-compatible angle (radians).

    For use in e.g. calls to `pygame.draw.arc`

    Parameters
    ----------
    bearing_deg: float
        Conventional bearing angle in degrees CCW from North

    Returns
    -------
    float
        Pygame-compatible angle in radians CW from East

    """
    return radians(-bearing_deg + 90)
