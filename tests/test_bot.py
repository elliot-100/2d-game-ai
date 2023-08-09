"""Tests for the Bot class in isolation."""

from pygame import Vector2

from src.bot import Bot
from tests import NE, NW, SE, SW, E, N, S, W


def test_create() -> None:
    """Test Bot initial state."""
    b = Bot(
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
    b = Bot(
        name="b0",
        pos=Vector2(0, 0),
    )

    assert [b.can_see(p) for p in (NW, N, NE)] == [True, True, True]
    assert [b.can_see(p) for p in (E, SE, S, SW, W)] == [
        False,
        False,
        False,
        False,
        False,
    ]


def test_move() -> None:
    """Test Bot linear move."""
    b = Bot(
        name="b0",
        pos=Vector2(0, 0),
    )
    b.velocity = Vector2(1, 0)
    b.move()
    assert b.pos == Vector2(1, 0)


def test_move_negative() -> None:
    """Test that Bot does not change position by default, as velocity is zero."""
    b = Bot(
        name="b0",
        pos=Vector2(0, 0),
    )
    b.move()
    assert b.pos == Vector2(0, 0)
