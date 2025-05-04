"""Tests for `World` class."""

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle
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


def test_add_obstacle_circle() -> None:
    """Test adding an ObstacleCircle to the World."""
    # arrange
    w = World(10)
    # act
    oc0 = ObstacleCircle(
        name="m0",
        position_from_sequence=(0, 0),
    )
    w.add_entity(oc0)
    # assert
    assert w.entities == {oc0}
    assert w.obstacles == {oc0}


def test_add_obstacle_rectangle() -> None:
    """Test adding an ObstacleRectangle to the World."""
    # arrange
    w = World(10)
    # act
    or0 = ObstacleRectangle(
        name="m0",
        position_from_sequence=(0, 0),
    )
    w.add_entity(or0)
    # assert
    assert w.entities == {or0}
    assert w.obstacles == {or0}


def test_point_is_inside_world_bounds() -> None:
    """Test that points are inside/outside World."""
    # arrange
    w = World(10)
    p0 = Vector2(0, 0)
    p1 = Vector2(-8, 8)
    # act/assert
    assert w.location_is_inside_world_bounds(p0)
    assert not w.location_is_inside_world_bounds(p1)
