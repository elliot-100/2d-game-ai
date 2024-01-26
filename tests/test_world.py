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


def test_point_is_outside_world_bounds() -> None:
    """Test that points are inside/outside World."""
    w = World(10)
    assert not w.point_is_outside_world_bounds(Vector2(0, 0))
    assert w.point_is_outside_world_bounds(Vector2(-8, 8))
