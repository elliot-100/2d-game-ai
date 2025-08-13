"""Tests for `WorldRenderer` class."""

from pygame import Vector2

from two_d_game_ai.view.world_renderer import WorldRenderer
from two_d_game_ai.world.world import World


def test_to_local() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    # arrange
    w = World(size_from_sequence=(20, 20))
    wr = WorldRenderer(world=w, scale_factor=1)
    world_origin = Vector2(0, 0)
    world_max = Vector2(10, 10)
    # act
    local_origin = wr.to_local(world_origin)
    local_max = wr.to_local(world_max)
    # assert
    assert local_origin == Vector2(10, 10)
    assert local_max == Vector2(20, 0)


def test_to_local_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at centre."""
    # arrange
    w = World(size_from_sequence=(20, 20))
    wr = WorldRenderer(world=w, scale_factor=2)
    world_origin = Vector2(0, 0)
    world_max = Vector2(10, 10)
    # act
    local_origin = wr.to_local(world_origin)
    local_max = wr.to_local(world_max)
    # assert
    assert local_origin == Vector2(20, 20)
    assert local_max == Vector2(40, 0)


def test_to_world() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    # arrange
    w = World(size_from_sequence=(20, 20))
    wr = WorldRenderer(world=w, scale_factor=1)
    local_origin = Vector2(0, 0)
    local_max = Vector2(20, 20)
    # act
    world_origin = wr.to_world(local_origin)
    world_max = wr.to_world(local_max)
    # assert
    assert world_origin == Vector2(-10, 10)
    assert world_max == Vector2(10, -10)


def test_from_display_with_scale_factor() -> None:
    """Test that coordinates are converted so that origin is at top left."""
    # arrange
    w = World(size_from_sequence=(20, 20))
    wr = WorldRenderer(world=w, scale_factor=2)
    window_origin = Vector2(0, 0)
    window_point = Vector2(40, 40)
    local_origin = wr.to_world(window_origin)
    local_point = wr.to_world(window_point)
    # act
    assert local_origin == Vector2(-10, 10)
    assert local_point == Vector2(10, -10)
