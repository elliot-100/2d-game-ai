"""Tests for the Bot class."""

from pygame import Vector2

from src.bot import Bot


def test_create() -> None:
    b = Bot(
        pos=Vector2(0.7, 100.35),
        radius=1.5,
    )
    assert b.pos == Vector2(0.7, 100.35)
    assert b.radius == 1.5
