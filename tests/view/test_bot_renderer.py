"""Tests for `BotRenderer` class."""

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that `BotRenderer` is created on `View` render.

    Can't be tested on `WorldRenderer.render(), as it does not create a Pygame window.
    """
    # arrange
    w = World(10)
    v = View(world=w)
    b = Bot(
        name="b1",
        position_from_sequence=(0.7, 100.35),
    )
    w.add_entity(b)
    # act
    v.render()
    # assert
    assert len(v.world_renderer.bot_renderers) == 1
    assert v.world_renderer.bot_renderers.pop().entity is b
