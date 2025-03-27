"""Tests for `World` class."""

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.world.world import World


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
        position_from_sequence=(0, 0),
    )
    assert w.entities == {b}
    assert w.bots == {b}


def test_add_movement_block() -> None:
    """Test adding a Bot to the World."""
    w = World(10)
    m = MovementBlock(
        world=w,
        name="m0",
        position_from_sequence=(0, 0),
    )
    assert w.entities == {m}
    assert w.movement_blocks == {m}


def test_point_is_inside_world_bounds() -> None:
    """Test that points are inside/outside World."""
    w = World(10)
    assert w.location_is_inside_world_bounds(Vector2(0, 0))
    assert not w.location_is_inside_world_bounds(Vector2(-8, 8))
