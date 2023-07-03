"""Tests for the World class."""

from pygame import Vector2

from src.world import World


def test_create() -> None:
    w = World(
        radius=0.5,
    )
    assert w.radius == 0.5


def test_add_bot() -> None:
    w = World(10)
    w.add_bot(
        pos=Vector2(0, 0),
        radius=1,
    )
    assert len(w.bots) == 1
