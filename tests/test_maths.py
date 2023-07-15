"""Tests for maths functions."""

from src.maths import relative_bearing_degrees
from tests import NE, NW, SE, SW, E, N, S, W

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
