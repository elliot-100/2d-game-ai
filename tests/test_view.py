"""Tests for the Renderer class."""

from pygame import Vector2

from two_d_game_ai.view import View
from two_d_game_ai.world import World


def test_to_display() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    world = World(radius=100)
    view = View(world)
    world_origin = Vector2(0, 0)
    assert view.to_display(world_origin) == Vector2(100, 100)
