"""Tests for `BotRenderer` class."""

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that `BotRenderer` is created on `View` initialization."""
    # arrange
    w = World(10)
    b = Bot(
        world=w,
        name="b1",
        position=(0.7, 100.35),
    )
    v = View(world=w, name="the_view")
    # act
    assert v.bot_renderers.pop().entity is b
