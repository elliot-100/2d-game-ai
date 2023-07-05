"""Tests for the Bot class."""

from pygame import Vector2

from src.bot import Bot


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
    # Test that Bot has default heading.
    assert b.heading == Bot.DEFAULT_HEADING == Vector2(0, 0)
