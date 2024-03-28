"""Tests for the View class."""

from pygame import Vector2

from two_d_game_ai.render.view import View
from two_d_game_ai.world import World


def test_to_display() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    w = World(radius=100)
    v = View(world=w, name="the_view")
    world_origin = Vector2(0, 0)
    assert v.to_display(world_origin) == Vector2(100, 100)
