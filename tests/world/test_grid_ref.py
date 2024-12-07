"""Tests for `GridRef` class."""

from two_d_game_ai.world.grid_ref import GridRef


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
