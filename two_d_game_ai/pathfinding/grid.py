"""Module containing `Grid` class."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2

from two_d_game_ai.geometry import lerp
from two_d_game_ai.pathfinding.grid_ref import GridRef

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class Grid:
    """Grid class.

    NB: there is no `Grid` cell class.

    """

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
        """Return `GridRef`s of all cells in the `Grid`."""
        return {
            GridRef(x, y) + self.offset
            for x in range(self.size)
            for y in range(self.size)
        }

    def in_bounds(self, cell: GridRef) -> bool:
        """Determine whether a cell is within the grid."""
        return abs(cell.x) <= self.size and abs(cell.y) <= self.size

    def reachable_neighbours(self, cell: GridRef) -> set[GridRef]:
        """Return a cell's reachable neighbours."""
        reachable_neighbours: set[GridRef] = set()

        if cell in self.untraversable_cells:
            return reachable_neighbours

        for dir_ in self._DIRECTIONS:
            neighbour = GridRef(cell.x + dir_[0], cell.y + dir_[1])
            if self.in_bounds(neighbour) and self._is_traversable(neighbour):
                reachable_neighbours.add(neighbour)
        return reachable_neighbours

    def _is_traversable(self, cell: GridRef) -> bool:
        """Determine whether a cell is traversable."""
        return cell not in self.untraversable_cells

    @staticmethod
    def cost(from_cell: GridRef, to_cell: GridRef) -> float:
        """Calculate the cost as Euclidean distance from one cell to another.

        NB: when calculating next step in a search, locations will be adjacent, so a
        cardinal move has basic cost = 1, and diagonal basic cost =~ 1.4.
        This function is generalised for wider use.

        """
        x_dist = abs(from_cell.x - to_cell.x)
        y_dist = abs(from_cell.y - to_cell.y)
        return math.sqrt(x_dist**2 + y_dist**2)

    def is_line_of_sight(self, world: World, cell_0: GridRef, cell_1: GridRef) -> bool:
        """Determine whether there is line-of-sight between two cells."""
        cells = Grid._cells_on_line(world, cell_0, cell_1)
        return any(cell not in self.untraversable_cells for cell in cells)

    @staticmethod
    def _cells_on_line(world: World, cell_0: GridRef, cell_1: GridRef) -> set[GridRef]:
        diagonal_distance = Grid._diagonal_distance(cell_0, cell_1)
        cells = set()
        for step in range(diagonal_distance):
            t = step / diagonal_distance
            point = Grid._lerp_grid_ref(cell_0, cell_1, t)
            point_v = Vector2(point[0], point[1])
            cells.add(GridRef.cell_from_pos(world, point_v))
        return cells

    @staticmethod
    def _diagonal_distance(cell_0: GridRef, cell_1: GridRef) -> int:
        delta = cell_1 - cell_0
        return max(abs(delta.x), abs(delta.y))

    @staticmethod
    def _lerp_grid_ref(
        cell_0: GridRef, cell_1: GridRef, t: float
    ) -> tuple[float, float]:
        return lerp(cell_0.x, cell_1.x, t), lerp(cell_0.y, cell_1.y, t)
