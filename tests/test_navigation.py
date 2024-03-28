"""Tests for navigation functions."""

from pygame import Vector2

from two_d_game_ai import navigation

VECTOR_NORTH = Vector2(0, 1)
VECTOR_EAST = Vector2(1, 0)
VECTOR_SOUTH = Vector2(0, -1)
VECTOR_WEST = Vector2(-1, 0)


def test_relative_bearing() -> None:
    """Test that relative bearings are calculated correctly."""
    vectors = (
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    )
    assert [navigation.relative_bearing(VECTOR_NORTH, v) for v in vectors] == [
        0,
        90,
        180,
        270,
    ]
    assert [navigation.relative_bearing(VECTOR_SOUTH, v) for v in vectors] == [
        180,
        270,
        0,
        90,
    ]


def test_relative_bearing_normalised() -> None:
    """Test that relative bearings are calculated correctly."""
    vectors = (
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    )
    assert [
        navigation.relative_bearing_normalised(VECTOR_NORTH, v) for v in vectors
    ] == [
        0,
        90,
        180,
        -90,
    ]
    assert [
        navigation.relative_bearing_normalised(VECTOR_SOUTH, v) for v in vectors
    ] == [
        180,
        -90,
        0,
        90,
    ]
