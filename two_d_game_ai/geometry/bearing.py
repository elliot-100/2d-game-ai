"""Module containing `Bearing` class."""

from __future__ import annotations

from dataclasses import dataclass, field

from pygame import Vector2

CIRCLE_DEGREES = 360


@dataclass
class Bearing:
    """Represents a conventional bearing (aka azimuthal angle).

    Stored as a unit vector, based on Pygame's Vector2 class.
    """

    vector: Vector2 = field(default_factory=Vector2, init=False)
    """The bearing as a standard (positive, right-handed, y-axis up) coordinate vector.
    """
    _degrees: float

    def __post_init__(self) -> None:
        """Construct vector from bearing angle."""
        v = Vector2()
        v.from_polar((1, self._degrees - CIRCLE_DEGREES / 4))
        self.vector = _flip_vector_y(v)

    @property
    def degrees(self) -> float:
        """Get bearing in degrees, positive clockwise from zero at North.

        0 <= degrees < 360.

        Intended for absolute bearings, where North is 0, East is 90, etc.
        """
        angle = -self.vector.as_polar()[1] + CIRCLE_DEGREES / 4
        if angle < 0:
            angle += CIRCLE_DEGREES
        if angle == CIRCLE_DEGREES:
            angle = 0
        return angle

    @property
    def degrees_normalised(self) -> float:
        """Get bearing in degrees, positive clockwise from zero at North.

        -180 <= degrees < 180, so due south is -180.

        Intended for relative bearings, where negative value is to left/port; positive
        is to right/starboard.
        """
        if self.degrees >= CIRCLE_DEGREES / 2:
            return self.degrees - CIRCLE_DEGREES
        return self.degrees

    def relative(self, other_vector: Vector2) -> Bearing:
        """Return new `Bearing` representing relative bearing to vector."""
        angle = -self.vector.angle_to(other_vector)
        return Bearing(angle)


def _flip_vector_y(vector: Vector2) -> Vector2:
    """Inverse the vector's y-axis to convert from Pygame's Vector2 implementation."""
    return Vector2(vector.x, -vector.y)
