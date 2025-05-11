"""Tests for `View` class."""

from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that `View` can be created and initialized."""
    # arrange
    w = World(20)
    # act
    v = View(world=w)
    # assert
    assert v
    assert v.world_renderer


def test_render() -> None:
    """Test that `View` can be rendered without error."""
    # arrange
    w = World(20)
    v = View(world=w)
    # act
    v.render()
    # assert
    assert v
