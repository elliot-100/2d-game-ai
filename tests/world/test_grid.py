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
        GridRef(x=-1, y=0),
        GridRef(x=0, y=-1),
        GridRef(x=-1, y=-1),
        GridRef(x=0, y=0),
    }


def test_cells_on_line() -> None:
    """Test that all cells between + including cell endpoints are returned."""
    # arrange
    g = Grid(size=4)
    c0 = GridRef(x=-1, y=-2)
    c1 = GridRef(x=1, y=1)
    # act
    cs = g._cells_on_line(c0, c1)
    # assert
    assert cs == {
        GridRef(x=-1, y=-2),
        GridRef(x=0, y=-1),
        GridRef(x=0, y=0),
        GridRef(x=1, y=1),
    }


def test_route__direct() -> None:
    """Test that only cell endpoints are returned when route is direct."""
    # arrange
    g = Grid(size=2)
    c0 = GridRef(x=-1, y=0)
    c1 = GridRef(x=1, y=1)
    # act
    cs = g.route(c0, c1)
    # assert
    assert cs == [
        GridRef(x=-1, y=-0),
        GridRef(x=1, y=1),
    ]


def test_cell_from_pos() -> None:
    """Test that `World` coordinates are converted to a `GridRef`."""
    # arrange
    w = World(size=100, grid_size=10)
    p = Vector2(15, 45)
    # act
    gr = Grid.cell_from_world_pos(w, p)
    # assert
    assert gr == GridRef(1, 4)


def test_cell_to_world_pos() -> None:
    """Test that world pos of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = Grid._cell_to_world_pos(gr, w)
    # assert
    assert p == Vector2(30, -70)


def test_cell_centre_to_world_pos() -> None:
    """Test that world pos of the centre of the cell is calculated correctly."""
    # arrange
    w = World(size=100, grid_size=10)
    gr = GridRef(3, -7)
    # act
    p = Grid.cell_centre_to_world_pos(gr, w)
    # assert
    assert p == Vector2(35, -65)
