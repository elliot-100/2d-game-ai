"""Tests for `Obstacle` class."""

from __future__ import annotations

from pygame import Vector2

from two_d_game_ai.entities.obstacle import Obstacle
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test Obstacle initial state."""
    # arrange
    w = World(10)
    # act
    m = Obstacle(world=w, name="m0", position_from_sequence=(5000, -9000), radius=1)
    assert m.name == "m0"
    assert m.position == Vector2(5000, -9000)
