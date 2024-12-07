"""Tests for `Grid` class."""

from two_d_game_ai.world.grid import Grid
from two_d_game_ai.world.grid_ref import GridRef


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
