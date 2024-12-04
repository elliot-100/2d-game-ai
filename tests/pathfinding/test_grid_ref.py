"""Tests for `GridRef` class."""

from pygame import Vector2

from two_d_game_ai.pathfinding import GridRef
from two_d_game_ai.world import World


def test_cell_to_pos() -> None:
    """Test that world pos of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = gr.cell_to_pos(w)
    # assert
    assert p == Vector2(30, -70)


def test_cell_centre_to_pos() -> None:
    """Test that world pos of the centre of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = gr.cell_centre_to_pos(w)
    # assert
    assert p == Vector2(35, -65)


def test_cell_from_pos() -> None:
    """Test that `World` coordinates are converted to a `GridRef`."""
    # arrange
    w = World(size=100, grid_size=10)
    p = Vector2(15, 45)
    # act
    gr = GridRef.cell_from_pos(w, p)
    # assert
    assert gr == GridRef(1, 4)
