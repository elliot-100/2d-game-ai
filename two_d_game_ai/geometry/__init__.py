"""Package containing geometric classes and functions."""

from math import radians

from pygame import Vector2

from two_d_game_ai.geometry.bearing import CIRCLE_DEGREES, Bearing

__all__ = ("CIRCLE_DEGREES", "Bearing", "point_in_or_on_circle")


def point_in_or_on_circle(
    *,
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Return `True` if `point` is (inside or on) the circle, else `False`."""
    return (point - circle_centre).length_squared() <= circle_radius**2


def to_display_radians(bearing_deg: float) -> float:
    """Convert bearing (degrees) to Pygame-compatible angle (radians).

    For use in e.g. calls to `pygame.draw.arc`.

    Parameters
    ----------
    bearing_deg
        Conventional bearing angle in degrees CCW from North

    Returns
    -------
    float
        Pygame-compatible angle in radians CW from East

    """
    return radians(-bearing_deg + CIRCLE_DEGREES / 4)


def lerp(start: int, end: int, t: float) -> float:
    """Linear interpolation between two values."""
    return start * (1.0 - t) + t * end
