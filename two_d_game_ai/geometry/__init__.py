"""Package containing geometric classes and functions."""

from pygame import Vector2


def point_in_or_on_circle(
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Return `True` if `point` is (inside or on) the circle, else `False`."""
    return (point - circle_centre).length() <= circle_radius
