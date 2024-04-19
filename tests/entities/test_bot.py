"""Tests for the Bot class in isolation."""

from tests import NE, NW, SE, SW, E, N, S, W
from two_d_game_ai import SIMULATION_STEP_INTERVAL_S, Vector2
from two_d_game_ai.entities import Bot
from two_d_game_ai.world import World


def test_create() -> None:
    """Test Bot initial state."""
    w = World(10)
    b = Bot(
        world=w,
        name="b1",
        pos=Vector2(0.7, 100.35),
    )

    assert b.name == "b1"
    assert b.pos == Vector2(0.7, 100.35)

    # Test that Bot is initially stationary.
    assert b._velocity == Vector2(0, 0)
    assert b._speed == 0
    # Test Bot defaults
    assert b.heading.vector == Vector2(0, 1)


def test_can_see_point__in_range() -> None:
    """Test Bot vision for points inside visual range.

    With default North heading, can see only points on/within 90 degree cone.
    """
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=Vector2(0, 0),
    )

    assert [b.can_see_point(p) for p in (NW, N, NE)] == [
        True,
        True,
        True,
    ]
    assert [b.can_see_point(p) for p in (E, SE, S, SW, W)] == [
        False,
        False,
        False,
        False,
        False,
    ]


def test_move() -> None:
    """Test Bot linear move."""
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=Vector2(0, 0),
    )
    b._velocity = Vector2(1, 0)
    b.move()
    assert b.pos == Vector2(SIMULATION_STEP_INTERVAL_S, 0)


def test_move_negative() -> None:
    """Test that Bot does not change position by default, as velocity is zero."""
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=Vector2(0, 0),
    )
    b.move()
    assert b.pos == Vector2(0, 0)
