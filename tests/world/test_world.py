"""Tests for `World` class."""

import pytest
from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle
from two_d_game_ai.world.grid_ref import GridRef
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test World initial state."""
    # arrange / act
    w = World(size_from_sequence=(5, 5))
    # assert
    assert w.size == Vector2(5, 5)


def test_add_bot() -> None:
    """Test adding a Bot to the World."""
    # arrange
    w = World(size_from_sequence=(10, 10))
    b = Bot(
        name="b0",
        position_from_sequence=(0, 0),
    )
    # act
    w.add_generic_entity(b)
    # assert
    assert w.generic_entities == {b}
    assert w.bots == {b}
    assert w.grid


def test_add_obstacle_circle() -> None:
    """Test adding an ObstacleCircle to the World."""
    # arrange
    w = World(size_from_sequence=(10, 10))
    # act
    oc0 = ObstacleCircle(
        name="m0",
        position_from_sequence=(0, 0),
    )
    w.add_generic_entity(oc0)
    # assert
    assert w.generic_entities == {oc0}
    assert w.obstacles == {oc0}


def test_add_obstacle_rectangle() -> None:
    """Test adding an ObstacleRectangle to the World."""
    # arrange
    w = World(size_from_sequence=(10, 10))
    # act
    or0 = ObstacleRectangle(
        name="m0",
        position_from_sequence=(0, 0),
    )
    w.add_generic_entity(or0)
    # assert
    assert w.generic_entities == {or0}
    assert w.obstacles == {or0}


def test_grid_ref_from_pos() -> None:
    """Test that World coordinates are converted to a `GridRef`."""
    # arrange
    w = World(size_from_sequence=(100, 100), grid_size=10)
    world_origin = Vector2(0, 0)
    # act
    origin_grid_ref = w.grid_ref_from_pos(world_origin)
    # assert
    assert origin_grid_ref == GridRef(5, 5)


def test_cell_from_pos__out_of_bounds() -> None:
    """Test that out-of-bounds coordinates...."""
    # arrange
    w = World(size_from_sequence=(100, 100), grid_size=10)
    pos = Vector2(0, -101)
    # act, assert
    with pytest.raises(ValueError, match="Can't get a `GridRef` for pos"):
        w.grid_ref_from_pos(pos)
