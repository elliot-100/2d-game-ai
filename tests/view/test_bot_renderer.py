"""Tests for `BotRenderer` class."""

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World


def test_create_() -> None:
    """Test that `BotRenderer` is created on `View` render."""
    # arrange
    w = World(10)
    v = View(world=w, name="the_view")
    b = Bot(
        world=w,
        name="b1",
        position_from_tuple=(0.7, 100.35),
    )
    # act
    v.render()
    assert len(v.bot_renderers) == 1
    assert v.bot_renderers.pop().entity is b
