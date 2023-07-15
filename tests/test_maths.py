"""Tests for maths functions."""

from pygame import Vector2

from src.maths import relative_bearing_degrees

"""Define compass directions as vectors in conventional Cartesian system."""

N = Vector2(0, 1)
NE = Vector2(1, 1)
E = Vector2(1, 0)
SE = Vector2(1, -1)
S = Vector2(0, -1)
SW = Vector2(-1, -1)
W = Vector2(-1, 0)
NW = Vector2(-1, 1)

compass = [N, NE, E, SE, S, SW, W, NW]


def test_relative_bearing_degrees() -> None:
    """Test that -180 < angle <=180."""
    assert [relative_bearing_degrees(N, d) for d in compass] == [
        0,
        -45,
        -90,
        -135,
        180,
        135,
        90,
        45,
    ]
    assert [relative_bearing_degrees(S, d) for d in compass] == [
        180,
        135,
        90,
        45,
        0,
        -45,
        -90,
        -135,
    ]
