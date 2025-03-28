"""Tests for `MovementBlockRenderer` class."""

from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that `MovementBlockRenderer` is created on `View.render()`.

    Can't be tested on `WorldRenderer.render(), as it does not create a Pygame window.
    """
    # arrange
    w = World(10)
    m = MovementBlock(
        world=w,
        name="b1",
        position_from_sequence=(0.7, 100.35),
        radius=0.1,
    )
    v = View(world=w)
    # act
    v.render()
    assert len(v.world_renderer.movement_block_renderers) == 1
    assert v.world_renderer.movement_block_renderers.pop().entity is m
