"""Tests for Obstacle renderer classes."""

from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create_circle() -> None:
    """Test that Obstacle renderer is created on `View.render()`.

    Can't be tested on `WorldRenderer.render(), as it does not create a Pygame window.
    """
    # arrange
    w = World(size_from_sequence=(10, 10))
    w.add_generic_entity(
        ObstacleCircle(name="oc0", position_from_sequence=(0.7, 100.35))
    )
    v = View(world=w)
    # act
    v.render()
    # assert
    assert v.world_renderer.obstacle_renderers.pop().entity.name == "oc0"


def test_create_rectangle() -> None:
    """Test that Obstacle renderers are created on `View.render()`.

    Can't be tested on `WorldRenderer.render(), as it does not create a Pygame window.
    """
    # arrange
    w = World(size_from_sequence=(10, 10))
    w.add_generic_entity(
        ObstacleRectangle(name="or0", position_from_sequence=(0.7, 100.35))
    )
    v = View(world=w)
    # act
    v.render()
    # assert
    assert v.world_renderer.obstacle_renderers.pop().entity.name == "or0"
