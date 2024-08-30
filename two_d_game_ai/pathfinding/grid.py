"""Module containing `Grid` class."""

from __future__ import annotations

from two_d_game_ai.pathfinding.grid_ref import GridRef


class Grid:
    """Grid class."""

    def __init__(
        self,
        size: int,
    ) -> None:
        self.size = size
        self.offset = GridRef(-size // 2, -size // 2)
        self.untraversable_cells: set[GridRef] = set()

    @property
    def cells(self) -> set[GridRef]:
        """Return all cells in the `Grid`."""
        return {
            GridRef(x, y) + self.offset
            for x in range(self.size)
            for y in range(self.size)
        }

    def in_bounds(self, location: GridRef) -> bool:
        """Determine whether a location is within the grid."""
        return abs(location.x) <= self.size and abs(location.y) <= self.size
