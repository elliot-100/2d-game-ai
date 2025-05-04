"""Tests for `MovementBlock` class."""

from __future__ import annotations

from pygame import Vector2

from two_d_game_ai.entities.movement_block import MovementBlock


def test_create() -> None:
    """Test MovementBlock initial state."""
    # arrange / act
    m = MovementBlock(name="m0", position_from_sequence=(5000, -9000), radius=1)
    # assert
    assert m.name == "m0"
    assert m.position == Vector2(5000, -9000)
