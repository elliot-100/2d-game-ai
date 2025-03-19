"""Tests for `MovementBlock` class."""

from __future__ import annotations

from pygame import Vector2

from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test MovementBlock initial state."""
    # arrange
    w = World(10)
    # act
    m = MovementBlock(world=w, name="m0", position=(5000, -9000), radius=1)
    assert m.name == "m0"
    assert m.pos == Vector2(5000, -9000)
