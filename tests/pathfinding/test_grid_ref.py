"""Tests for `GridRef` class."""

from pygame import Vector2

from two_d_game_ai.pathfinding import GridRef
from two_d_game_ai.world import World


def test_add() -> None:
    """Test addition."""
    # arrange
    gr0 = GridRef(3, -7)
    gr1 = GridRef(-6, 2)
    # act
    gr = gr0 + gr1
    # assert
    assert gr == GridRef(-3, -5)


def test_subtract() -> None:
    """Test addition."""
    # arrange
    gr0 = GridRef(3, -7)
    gr1 = GridRef(-6, 2)
    # act
    gr = gr0 - gr1
    # assert
    assert gr == GridRef(9, -9)


def test_cell_to_pos() -> None:
    """Test that world pos of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = gr._cell_to_world_pos(w)
    # assert
    assert p == Vector2(30, -70)


def test_cell_centre_to_pos() -> None:
    """Test that world pos of the centre of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = gr.cell_centre_to_world_pos(w)
    # assert
    assert p == Vector2(35, -65)


def test_cell_from_pos() -> None:
    """Test that `World` coordinates are converted to a `GridRef`."""
    # arrange
    w = World(size=100, grid_size=10)
    p = Vector2(15, 45)
    # act
    gr = GridRef.cell_from_world_pos(w, p)
    # assert
    assert gr == GridRef(1, 4)
