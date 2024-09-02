"""Module containing `Grid` class."""

from __future__ import annotations

import math
from typing import ClassVar

from two_d_game_ai.pathfinding.grid_ref import GridRef


class Grid:
    """Grid class."""

    _DIRECTIONS: ClassVar = {
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
    }

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

    def reachable_neighbours(self, location: GridRef) -> set[GridRef]:
        """Return a location's reachable neighbours."""
        reachable_neighbours: set[GridRef] = set()

        if location in self.untraversable_cells:
            return reachable_neighbours

        for dir_ in self._DIRECTIONS:
            neighbour = GridRef(location.x + dir_[0], location.y + dir_[1])
            if self.in_bounds(neighbour) and self._is_traversable(neighbour):
                reachable_neighbours.add(neighbour)
        return reachable_neighbours

    def _is_traversable(self, location: GridRef) -> bool:
        """Determine whether a location is traversable."""
        return location not in self.untraversable_cells

    @staticmethod
    def cost(from_location: GridRef, to_location: GridRef) -> float:
        """Calculate the cost as Euclidean distance from one location to another.

        NB: when calculating next step in a search, locations will be adjacent, so a
        cardinal move has basic cost = 1, and diagonal basic cost =~ 1.4.
        This function is generalised for wider use.

        """
        x_dist = abs(from_location.x - to_location.x)
        y_dist = abs(from_location.y - to_location.y)
        return math.sqrt(x_dist**2 + y_dist**2)
