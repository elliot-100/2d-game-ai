"""Tests for `WorldRenderer` class."""

from pygame import Vector2

from two_d_game_ai.view.world_renderer import WorldRenderer
from two_d_game_ai.world.world import World


def test_to_local() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    # arrange
    w = World(200)
    wr = WorldRenderer(world=w)
    world_origin = Vector2(0, 0)
    world_max = Vector2(100, 100)
    # act
    local_origin = wr.to_local(world_origin)
    local_max = wr.to_local(world_max)
    assert local_origin == Vector2(100, 100)
    assert local_max == Vector2(200, 0)


def test_to_local_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    # arrange
    w = World(200)
    wr = WorldRenderer(world=w, scale_factor=2)
    world_origin = Vector2(0, 0)
    world_max = Vector2(100, 100)
    # act
    local_origin = wr.to_local(world_origin)
    local_max = wr.to_local(world_max)
    assert local_origin == Vector2(200, 200)
    assert local_max == Vector2(400, 0)


def test_to_world() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    # arrange
    w = World(200)
    wr = WorldRenderer(world=w)
    local_origin = Vector2(0, 0)
    local_max = Vector2(200, 200)
    # act
    world_origin = wr.to_world(local_origin)
    world_max = wr.to_world(local_max)
    assert world_origin == Vector2(-100, 100)
    assert world_max == Vector2(100, -100)


def test_from_display_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    # arrange
    w = World(200)
    wr = WorldRenderer(world=w, scale_factor=2)
    window_origin = Vector2(0, 0)
    window_point = Vector2(400, 400)
    # act
    assert wr.to_world(window_origin) == Vector2(-100, 100)
    assert wr.to_world(window_point) == Vector2(100, -100)
