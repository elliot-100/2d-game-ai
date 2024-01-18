"""Tests for the World class."""

from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bot import Bot
from two_d_game_ai.world import World


def test_create() -> None:
    """Test World initial state."""
    w = World(
        radius=0.5,
    )
    assert w.radius == 0.5


def test_add_bot() -> None:
    """Test adding a Bot to the World."""
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=Vector2(0, 0),
    )
    assert w.bots == [b]


# TODO: doesn't belong here
def test_update() -> None:
    """Test Bot linear move in World context."""
    w = World(10)
    b = Bot(
        w,
        name="b0",
        pos=Vector2(0, 0),
    )
    b.velocity = Vector2(1, 0)
    w.update()
    assert b.pos == Vector2(SIMULATION_STEP_INTERVAL_S, 0)
