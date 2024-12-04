"""Tests for `Grid` class."""

from two_d_game_ai.pathfinding import Grid, GridRef


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
