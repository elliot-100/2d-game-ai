"""Tests for `Grid` class."""

from pygame import Vector2

from two_d_game_ai.world.grid import Grid
from two_d_game_ai.world.grid_ref import GridRef
from two_d_game_ai.world.world import World


def test_cells() -> None:
    """Test that all cells in the `Grid` are returned."""
    # arrange
    g = Grid(size=2)
    # act
    cs = g.cells
    # assert
    assert cs == {
        GridRef(x=0, y=0),
        GridRef(x=0, y=1),
        GridRef(x=1, y=0),
        GridRef(x=1, y=1),
    }


def test_cells_on_line() -> None:
    """Test that all cells between + including cell endpoints are returned."""
    # arrange
    g = Grid(size=8)
    c0 = GridRef(x=0, y=0)
    c1 = GridRef(x=2, y=3)
    # act
    cs = g._cells_on_line(c0, c1)
    # assert
    assert cs == {
        GridRef(x=0, y=0),
        GridRef(x=0, y=1),
        GridRef(x=1, y=2),
        GridRef(x=2, y=3),
    }


def test_cell_from_pos() -> None:
    """Test that `World` coordinates are converted to a `GridRef`."""
    # arrange
    w = World(size=100, grid_size=10)
    world_origin = Vector2(0, 0)
    # act
    origin_grid_ref = Grid.grid_ref_from_world_pos(world=w, pos=world_origin)
    # assert
    assert origin_grid_ref == GridRef(5, 5)


def test_cell_centre_to_world_pos() -> None:
    """Test that world pos of the centre of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    min_cell = GridRef(0, 0)
    # act
    world_pos = Grid.cell_centre_to_world_pos(world=w, grid_ref=min_cell)
    # assert
    assert world_pos == Vector2(-45, -45)
