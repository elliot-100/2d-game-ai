"""Tests for the Bot class in isolation."""

from pygame import Vector2

from tests import NE, NW, SE, SW, E, N, S, W
from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bot import Bot
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
    assert b.velocity == Vector2(0, 0)
    assert b.speed == 0
    # Test Bot defaults
    assert b.heading == Bot.INITIAL_HEADING == Vector2(0, 1)


def test_can_see() -> None:
    """Test Bot vision.

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
    b.velocity = Vector2(1, 0)
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


def test_is_outside_world_bounds() -> None:
    """Test that Bots are inside/outside World."""
    w = World(10)
    b0 = Bot(
        world=w,
        name="b0",
        pos=Vector2(5, -5),
    )
    b1 = Bot(
        world=w,
        name="b0",
        pos=Vector2(-8, 9),
    )
    assert not b0.is_outside_world_bounds
    assert b1.is_outside_world_bounds
