"""Bearing class."""

from __future__ import annotations

from pygame import Vector2

CIRCLE_DEGREES = 360


class Bearing:
    """Represents a conventional bearing (aka azimuthal angle).

    Stored as a unit vector, based on Pygame's Vector2 class.

    Attributes/properties
    ---------------------
    degrees: float
        The bearing in positive degrees clockwise from zero at North
        0 <= degrees < 360
    degrees_normalised: float
        The bearing in degrees from zero at North
        -180 <= degrees < 180
        Negative value is to left/port/counter-clockwise
        Positive value is to right/starboard/clockwise

    vector: Vector2
        The bearing as a standard (positive, right-handed, y-axis up) coordinate vector
    """

    # degrees: float
    # vector: Vector2

    def __init__(self, degrees: float) -> None:
        v = Vector2()
        v.from_polar((1, degrees - CIRCLE_DEGREES / 4))
        self.vector = _flip_vector_y(v)

    @property
    def degrees(self) -> float:
        """Return the bearing in degrees clockwise from North.

        0 <= degrees < 360
        """
        angle = -self.vector.as_polar()[1] + CIRCLE_DEGREES / 4
        if angle < 0:
            angle += CIRCLE_DEGREES
        if angle == CIRCLE_DEGREES:
            angle = 0
        return angle

    @property
    def degrees_normalised(self) -> float:
        """Return -180 <= degrees < 180."""
        if self.degrees >= CIRCLE_DEGREES / 2:
            return self.degrees - CIRCLE_DEGREES
        return self.degrees

    def relative(self, other_vector: Vector2) -> Bearing:
        """Return new Bearing representing relative bearing to vector."""
        angle = -self.vector.angle_to(other_vector)
        return Bearing(angle)


def _flip_vector_y(vector: Vector2) -> Vector2:
    """Inverse the vector's y-axis to convert from Pygame's Vector2 implementation."""
    return Vector2(vector.x, -vector.y)