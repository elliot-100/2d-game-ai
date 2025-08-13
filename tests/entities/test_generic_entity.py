"""Tests for `GenericEntity` class."""

from __future__ import annotations

from pygame import Vector2

from two_d_game_ai.entities.generic_entity import GenericEntity


def test_create() -> None:
    """Test GenericEntity initial state."""
    # arrange / act
    g = GenericEntity(
        name="g1",
        position_from_sequence=(0.7, 100.35),
    )
    # assert
    assert g.name == "g1"
    assert g.position == Vector2(0.7, 100.35)
