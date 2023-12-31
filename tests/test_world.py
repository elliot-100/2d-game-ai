"""Tests for the World class."""

from pygame import Vector2

from src import SIMULATION_STEP_INTERVAL_S
from src.world import World


def test_create() -> None:
    """Test World initial state."""
    w = World(
        radius=0.5,
    )
    assert w.radius == 0.5


def test_add_bot() -> None:
    """Test adding a Bot to the World."""
    w = World(10)
    w.add_bot(
        name="b0",
        pos=Vector2(0, 0),
    )
    assert len(w.bots) == 1
    assert w.bots["b0"].name == "b0"


def test_update() -> None:
    """Test Bot linear move in World context."""
    w = World(10)
    w.add_bot(
        name="b0",
        pos=Vector2(0, 0),
    )
    b = w.bots["b0"]
    b.velocity = Vector2(1, 0)
    w.update()
    assert b.pos == Vector2(SIMULATION_STEP_INTERVAL_S, 0)
