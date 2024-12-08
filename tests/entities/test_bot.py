"""Tests for `Bot` class."""

from __future__ import annotations

import pytest
from pygame import Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.world.world import World


@pytest.fixture
def compass_directions() -> dict[str, Vector2]:
    """Define compass directions as vectors in conventional Cartesian system."""
    return {
        "N": Vector2(0, 1),
        "NE": Vector2(1, 1),
        "E": Vector2(1, 0),
        "SE": Vector2(1, -1),
        "S": Vector2(0, -1),
        "SW": Vector2(-1, -1),
        "W": Vector2(-1, 0),
        "NW": Vector2(-1, 1),
    }


def test_create() -> None:
    """Test Bot initial state."""
    # arrange
    w = World(10)
    # act
    b = Bot(
        world=w,
        name="b1",
        position=(0.7, 100.35),
    )
    assert b.name == "b1"
    assert b.pos == Vector2(0.7, 100.35)
    # Bot is initially stationary:
    assert b.velocity == Vector2(0, 0)
    # Defaults:
    assert b.heading.vector == Vector2(0, 1)
    assert b.radius == 0


def test_can_see_point__in_range(
    compass_directions: dict[str, Vector2],
) -> None:
    """Test Bot vision for points inside visual range.

    With default North heading, can see only points on/within 90 degree cone.
    """
    # arrange
    w = World(10)
    visible_points = [compass_directions[_] for _ in ["NW", "N", "NE"]]
    not_visible_points = [compass_directions[_] for _ in ["E", "SE", "S", "SW", "W"]]
    # act
    b = Bot(
        world=w,
        name="b0",
        position=(0, 0),
    )
    # assert
    assert all(b.can_see_point(p) for p in visible_points)
    assert not any(b.can_see_point(p) for p in not_visible_points)


def test_move() -> None:
    """Test Bot linear move."""
    # arrange
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        position=(0, 0),
    )
    b.velocity = Vector2(1, 0)
    # act
    b._move()
    # assert
    assert b.pos == Vector2(1 / SIMULATION_FPS, 0)


def test_move_negative() -> None:
    """Test that Bot does not change position by default, as velocity is zero."""
    # arrange
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        position=(0, 0),
    )
    # act
    b._move()
    # assert
    assert b.pos == Vector2(0, 0)


def test_destination() -> None:
    """Test that Bot can be given destination inside World limits."""
    # arrange
    w = World(40)
    b = Bot(
        world=w,
        name="b0",
        position=(0, 0),
    )
    # act
    b.destination = Vector2(-17, -12)
    # assert
    assert b.destination == Vector2(-17, -12)


def test_set_destination_tuple() -> None:
    """Test that Bot can be given destination as tuple inside World limits."""
    # arrange
    w = World(100)
    b = Bot(
        world=w,
        name="b0",
        position=(0, 0),
    )
    # act
    b.set_destination(25, -50)
    # assert
    assert b.destination == Vector2(25, -50)
