"""Tests for `World` class."""

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test World initial state."""
    # arrange / act
    w = World(5)
    # assert
    assert w.size == 5


def test_add_bot() -> None:
    """Test adding a Bot to the World."""
    # arrange
    w = World(10)
    b = Bot(
        name="b0",
        position_from_sequence=(0, 0),
    )
    # act
    w.add_entity(b)
    # assert
    assert w.entities == {b}
    assert w.bots == {b}


def test_add_movement_block() -> None:
    """Test adding a MovementBlock to the World."""
    # arrange
    w = World(10)
    # act
    m = MovementBlock(
        name="m0",
        position_from_sequence=(0, 0),
    )
    w.add_entity(m)
    # assert
    assert w.entities == {m}
    assert w.movement_blocks == {m}


def test_point_is_inside_world_bounds() -> None:
    """Test that points are inside/outside World."""
    # arrange
    w = World(10)
    p0 = Vector2(0, 0)
    p1 = Vector2(-8, 8)
    # act/assert
    assert w.location_is_inside_world_bounds(p0)
    assert not w.location_is_inside_world_bounds(p1)
