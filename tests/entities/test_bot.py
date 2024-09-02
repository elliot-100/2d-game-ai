"""Tests for `Bot` class."""

from __future__ import annotations

import pytest

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S, Vector2
from two_d_game_ai.entities import Bot
from two_d_game_ai.world import World


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
        pos=(0.7, 100.35),
    )
    assert b.name == "b1"
    assert b.pos_v == Vector2(0.7, 100.35)
    # Bot is initially stationary:
    assert b._velocity_v == Vector2(0, 0)
    # Defaults:
    assert b.heading.vector == Vector2(0, 1)


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
        pos=(0, 0),
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
        pos=(0, 0),
    )
    b._velocity_v = Vector2(1, 0)
    # act
    b._move()
    # assert
    assert b.pos_v == Vector2(SIMULATION_STEP_INTERVAL_S, 0)


def test_move_negative() -> None:
    """Test that Bot does not change position by default, as velocity is zero."""
    # arrange
    w = World(10)
    b = Bot(
        world=w,
        name="b0",
        pos=(0, 0),
    )
    # act
    b._move()
    # assert
    assert b.pos_v == Vector2(0, 0)


def test_give_destination() -> None:
    """Test that Bot can be given destination inside World limits and this also sets
    destination_v.
    """
    # arrange
    w = World(100)
    b = Bot(
        world=w,
        name="b0",
        pos=(0, 0),
    )
    # act
    b.destination = (25, -50)
    # assert
    assert b.destination == (25, -50)
    assert b.destination_v == Vector2(25, -50)


def test_give_destination_v() -> None:
    """Test that Bot can be given destination vector (used in UI) inside World limits,
    and this also sets destination_v.
    """
    # arrange
    w = World(40)
    b = Bot(
        world=w,
        name="b0",
        pos=(0, 0),
    )
    # act
    b.destination_v = Vector2(-17, -12)
    # assert
    assert b.destination_v == Vector2(-17, -12)
    assert b.destination == (-17, -12)
