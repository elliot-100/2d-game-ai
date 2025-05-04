"""Tests for `ObstacleCircle` class."""

from __future__ import annotations

from pygame import Vector2

from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle


def test_create_circle() -> None:
    """Test ObstacleCircle is created."""
    # arrange / act
    oc0 = ObstacleCircle(name="m0", position_from_sequence=(5000, -9000))
    # assert
    assert oc0.name == "m0"
    assert oc0.position == Vector2(5000, -9000)


def test_create_rectangule() -> None:
    """Test ObstacleRectangle is created.."""
    # arrange / act
    or0 = ObstacleRectangle(name="m0", position_from_sequence=(5000, -9000))
    # assert
    assert or0.name == "m0"
    assert or0.position == Vector2(5000, -9000)
