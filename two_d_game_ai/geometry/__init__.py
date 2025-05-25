"""Package containing geometric classes and functions."""

from collections.abc import Iterable

from pygame import Vector2


def point_in_or_on_circle(
    *,
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Return `True` if `point` is (inside or on) the circle, else `False`."""
    return (point - circle_centre).length() <= circle_radius


def point_in_or_on_rect(
    *,
    point: Vector2,
    rect_min: Vector2,
    rect_size: Vector2,
) -> bool:
    """Return `True` if `point` is (inside or on) the rectangle, else `False`."""
    return (
        rect_min[0] <= point[0] <= (rect_min + rect_size)[0]
        and rect_min[1] <= point[1] <= (rect_min + rect_size)[1]
    )


def points_as_str(
    points: Iterable[Vector2],
) -> str:
    """Format points as a string for logging etc."""
    return ",".join(str(p) for p in points)
