"""Bearing class."""

from __future__ import annotations

from dataclasses import dataclass

from pygame import Vector2

CIRCLE_DEGREES = 360


@dataclass
class Bearing(float):
    """A conventional bearing (aka azimuthal angle) in degrees clockwise.
    Absolute bearings measured from North.


    """

    value: float = 0

    def __post_init__(self) -> None:
        """After initialisation, ensure 0.0 <= value < 360.0."""
        if self.value < 0:
            self.value += CIRCLE_DEGREES
        elif self.value > CIRCLE_DEGREES:
            self.value -= CIRCLE_DEGREES

    @property
    def value_normalized_180(self) -> float:
        """Return bearing value -180 <= value <= 180."""
        return self.value - CIRCLE_DEGREES / 2

    @classmethod
    def from_vector(cls, vector: Vector2) -> Bearing:
        """Return a Bearing from conventional Cartesian coordinates.

        Parameters
        ----------
        vector: Vector2
            Coordinate vector

        Returns
        -------
        Bearing
        """
        angle = -vector.as_polar()[1] + CIRCLE_DEGREES / 4
        if angle < 0:
            angle += CIRCLE_DEGREES
        return cls(angle)

    @classmethod
    # TODO: Not sure if needed?
    def relative(cls, heading: Vector2, displacement: Vector2) -> Bearing:
        """Return Bearing of the displacement, relative to vector heading.

        Returns
        -------
        The relative bearing in degrees clockwise
        0 >= bearing < 360
        """
        angle = -heading.angle_to(displacement)
        if angle < 0:
            angle += CIRCLE_DEGREES
        return cls(angle)

    def to_vector(self) -> Vector2:
        """Return conventional Cartesian coordinates.

        Returns
        -------
        Coordinate vector.
        """
        vector2 = Vector2()
        vector2.from_polar((1, self - CIRCLE_DEGREES / 4))
        return Vector2(vector2.x, -vector2.y)
