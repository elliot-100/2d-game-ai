"""Generalised maths functions."""

from pygame import Vector2

CIRCLE_DEGREES = 360


def relative_bearing_degrees(heading: Vector2, displacement: Vector2) -> float:
    """Return bearing of the displacement, relative to heading, in degrees CCW.

    -180 < bearing <= 180.
    """
    angle = heading.angle_to(displacement)
    if angle > CIRCLE_DEGREES / 2:
        angle -= CIRCLE_DEGREES
    elif angle <= -CIRCLE_DEGREES / 2:
        angle += CIRCLE_DEGREES
    return angle
