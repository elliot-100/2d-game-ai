"""Tests for the Bot class."""

from pygame import Vector2

from src.bot import Bot


def test_create() -> None:
    """Test Bot initial state."""
    b = Bot(
        pos=Vector2(0.7, 100.35),
    )
    assert b.pos == Vector2(0.7, 100.35)
