"""Bearing class."""

from __future__ import annotations

from dataclasses import dataclass, field

from two_d_game_ai import Vector2

_CIRCLE_DEGREES = 360


@dataclass
class Bearing:
    """Represents a conventional bearing (aka azimuthal angle).

    Stored as a unit vector, based on Pygame's Vector2 class.

    Attributes
    ----------
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

    vector: Vector2 = field(default_factory=Vector2, init=False)
    _degrees: float

    def __post_init__(self) -> None:
        """Construct vector from bearing angle."""
        v = Vector2()
        v.from_polar((1, self._degrees - _CIRCLE_DEGREES / 4))
        self.vector = _flip_vector_y(v)

    @property
    def degrees(self) -> float:
        """Get bearing: 0 <= degrees < 360, clockwise.

        Intended for absolute bearings, where North is 0, East is 90, etc.

        """
        angle = -self.vector.as_polar()[1] + _CIRCLE_DEGREES / 4
        if angle < 0:
            angle += _CIRCLE_DEGREES
        if angle == _CIRCLE_DEGREES:
            angle = 0
        return angle

    @property
    def degrees_normalised(self) -> float:
        """Get bearing: -180 <= degrees < 180, positive clockwise.

        Intended for relative bearings, where negative value is to left/port; positive
        is to right/starboard.

        Note: Due south is -180.

        """
        if self.degrees >= _CIRCLE_DEGREES / 2:
            return self.degrees - _CIRCLE_DEGREES
        return self.degrees

    def relative(self, other_vector: Vector2) -> Bearing:
        """Return new Bearing representing relative bearing to vector."""
        angle = -self.vector.angle_to(other_vector)
        return Bearing(angle)


def _flip_vector_y(vector: Vector2) -> Vector2:
    """Inverse the vector's y-axis to convert from Pygame's Vector2 implementation."""
    return Vector2(vector.x, -vector.y)
