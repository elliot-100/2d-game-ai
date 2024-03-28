"""Basic Cartesian navigation functions wrapped around Pygame.Vector2 library."""

from pygame import Vector2

CIRCLE_DEGREES = 360


def relative_bearing(heading: Vector2, displacement: Vector2) -> float:
    """Return bearing of the displacement, relative to heading, in degrees clockwise.

    Returns
    -------
    The relative bearing in degrees clockwise
    0 >= bearing < 360
    """
    angle = -heading.angle_to(displacement)
    if angle < 0:
        angle += CIRCLE_DEGREES
    return angle


def relative_bearing_normalised(heading: Vector2, displacement: Vector2) -> float:
    """Return bearing of the displacement, relative to heading, in degrees.

    Returns
    -------
    The relative bearing in degrees clockwise(if positive) or counterclockwise
    (if negative).
    -180 < bearing <= 180
    """
    angle = relative_bearing(heading, displacement)
    if angle > CIRCLE_DEGREES / 2:
        angle -= CIRCLE_DEGREES
    return angle


def point_in_or_on_circle(
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Determine if a point is (inside or on) a circle.

    Parameters
    ----------
    point
    circle_centre
    circle_radius

    Returns
    -------
    bool
        True if the point is (inside or on) the circle
    """
    return (point - circle_centre).length() <= circle_radius
