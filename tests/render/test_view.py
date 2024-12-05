"""Tests for `View` class."""

from pygame import Vector2

from two_d_game_ai.render import View
from two_d_game_ai.world import World


def test_to_display() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    w = World(200)
    v = View(world=w, name="the_view")
    world_origin = Vector2(0, 0)
    world_point = Vector2(100, 100)
    assert v.to_display(world_origin) == Vector2(100, 100)
    assert v.to_display(world_point) == Vector2(200, 0)


def test_to_display_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    w = World(200)
    v = View(world=w, name="the_view", scale_factor=2)
    world_origin = Vector2(0, 0)
    world_point = Vector2(100, 100)
    assert v.to_display(world_origin) == Vector2(200, 200)
    assert v.to_display(world_point) == Vector2(400, 0)


def test_from_display() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    w = World(200)
    v = View(world=w, name="the_view")
    window_origin = Vector2(0, 0)
    window_point = Vector2(200, 200)
    assert v._from_display(window_origin) == Vector2(-100, 100)
    assert v._from_display(window_point) == Vector2(100, -100)


def test_from_display_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    w = World(200)
    v = View(world=w, name="the_view", scale_factor=2)
    window_origin = Vector2(0, 0)
    window_point = Vector2(400, 400)
    assert v._from_display(window_origin) == Vector2(-100, 100)
    assert v._from_display(window_point) == Vector2(100, -100)
