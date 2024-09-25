"""Package containing geometric classes and functions."""

from two_d_game_ai import Vector2

from .bearing import Bearing

__all__ = ("Bearing",)



def point_in_or_on_circle(
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Return True if the point is (inside or on) the circle, else False."""
    return (point - circle_centre).length() <= circle_radius
