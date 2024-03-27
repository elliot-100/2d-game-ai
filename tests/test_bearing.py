"""Tests for Bearing class."""

from pygame import Vector2

from two_d_game_ai.navigation.bearing import Bearing

VECTOR_NORTH = Vector2(0, 1)
VECTOR_EAST = Vector2(1, 0)
VECTOR_SOUTH = Vector2(0, -1)
VECTOR_WEST = Vector2(-1, 0)


def test_from_vector() -> None:
    """Test that vectors are converted to bearings in degrees."""
    vectors = (
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    )
    assert [Bearing.from_vector(v).value for v in vectors] == [
        0,
        90,
        180,
        270,
    ]


def test_relative() -> None:
    """Test that relative bearings are calculated correctly.

    Should give 0 <= b < 360

    """
    vectors = (
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    )
    assert [Bearing.relative(VECTOR_NORTH, v).value for v in vectors] == [
        0,
        90,
        180,
        270,
    ]
    assert [Bearing.relative(VECTOR_SOUTH, v).value for v in vectors] == [
        180,
        270,
        0,
        90,
    ]


def test_to_vector() -> None:
    """Test that bearings in degrees are converted to vectors."""
    bearings = [
        0,
        90,
        180,
        270,
    ]
    assert [Bearing(b).to_vector() for b in bearings] == [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    ]


def test_to_vector__large_and_negative_values() -> None:
    """Test that bearings in degrees are converted to vectors."""
    bearings = [
        360,
        -270,
        540,
        -90,
    ]
    assert [Bearing(b).to_vector() for b in bearings] == [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    ]


def test_is_to_left() -> None:
    """TODO: Docstring for is_to_left."""
    bearings = [
        90,
        270,
    ]
    assert [Bearing(b).is_to_left(Bearing(0)) for b in bearings] == [False, True]
    assert [Bearing(b).is_to_left(Bearing(180)) for b in bearings] == [True, False]
