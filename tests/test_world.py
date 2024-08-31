"""Tests for `World` class."""

from two_d_game_ai.entities import Bot
from two_d_game_ai.world import World


def test_create() -> None:
    """Test World initial state."""
    w = World(5)
    assert w.size == 5


def test_add_bot() -> None:
    """Test adding a Bot to the World."""
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=(0, 0),
    )
    assert w.bots == [b]
