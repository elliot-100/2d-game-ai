"""Tests for `Bearing` class."""

import pytest
from pygame import Vector2

from two_d_game_ai.geometry.bearing import Bearing

VECTOR_NORTH = Vector2(0, 1)
VECTOR_EAST = Vector2(1, 0)
VECTOR_SOUTH = Vector2(0, -1)
VECTOR_WEST = Vector2(-1, 0)


def test_bearing_create_cardinal() -> None:
    """Test that cardinal vector bearings are created correctly from degrees."""
    degs = [0, 90, 180, 270]
    assert [Bearing(d).vector for d in degs] == [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    ]


def test_bearing_create_cardinal_large_values() -> None:
    """Test that cardinal vector bearings are created correctly from degrees >= 360."""
    degs = [360, 450, 540, 630, 720]
    assert [Bearing(d).vector for d in degs] == [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
        VECTOR_NORTH,
    ]


def test_bearing_create_cardinal_negative_values() -> None:
    """Test that cardinal vector bearings are created correctly from degrees < 0."""
    degs = [-360, -270, -180, -90]
    assert [Bearing(d).vector for d in degs] == [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    ]


def test_bearing_cardinal_degrees_preserved() -> None:
    """0 <= degrees < 360."""
    degs = [0, 90, 180, 270, 360]
    assert [Bearing(d).degrees for d in degs] == [0, 90, 180, 270, 0]


def test_bearing_degrees_normalised() -> None:
    """-180 <= degrees < 180."""
    degs = [0, 90, 180, 270, 360]
    assert [Bearing(d).degrees_normalised for d in degs] == [0, 90, -180, -90, 0]


def test_relative() -> None:
    """Test that relative bearings are calculated correctly."""
    vecs = [
        VECTOR_NORTH,
        VECTOR_EAST,
        VECTOR_SOUTH,
        VECTOR_WEST,
    ]
    # relative bearings from NORTH:
    assert [Bearing(0).relative(v).degrees for v in vecs] == [0, 90, 180, 270]
    # relative bearings from SOUTH:
    # TODO: fix fudging here?
    assert [Bearing(180).relative(v).degrees for v in vecs] == pytest.approx(
        [180, 270, 0, 90]
    )
