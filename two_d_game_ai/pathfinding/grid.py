"""Module containing `Grid` class."""

from __future__ import annotations

import logging
import math
from typing import ClassVar

from two_d_game_ai.geometry import lerp
from two_d_game_ai.pathfinding.grid_ref import GridRef
from two_d_game_ai.pathfinding.priority_queue import PriorityQueue


class Grid:
    """Grid class.

    NB: there is no 'Grid cell' class.

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
        """`Grid` units per side."""
        self.untraversable_cells: set[GridRef] = set()
        """Untraversable cells."""
        self._offset = GridRef(-size // 2, -size // 2)

    @property
    def cells(self) -> set[GridRef]:
        """Return `GridRef`s of all cells in the `Grid`."""
        return {
            GridRef(x, y) + self._offset
            for x in range(self.size)
            for y in range(self.size)
        }

    def _cell_is_in_bounds(self, cell: GridRef) -> bool:
        """Determine whether a cell is within the `Grid`."""
        return abs(cell.x) <= self.size and abs(cell.y) <= self.size

    def reachable_neighbours(self, cell: GridRef) -> set[GridRef]:
        """Return a cell's reachable neighbours."""
        reachable_neighbours: set[GridRef] = set()

        if cell in self.untraversable_cells:
            return reachable_neighbours

        for dir_ in self._DIRECTIONS:
            neighbour = GridRef(cell.x + dir_[0], cell.y + dir_[1])
            if self._cell_is_in_bounds(neighbour) and self._is_traversable(neighbour):
                reachable_neighbours.add(neighbour)
        return reachable_neighbours

    def _is_traversable(self, cell: GridRef) -> bool:
        """Determine whether a cell is traversable."""
        return cell not in self.untraversable_cells

    def route(
        self,
        from_cell: GridRef,
        to_cell: GridRef,
    ) -> list[GridRef]:
        """Determine a cell-based route between two cells.

        Returns
        -------
        list[GridRef]
            Cells on the path to `to_cell`, including `to_cell` itself.
            Empty if no path found.
        """
        # Early return cases:
        if from_cell in self.untraversable_cells or to_cell in self.untraversable_cells:
            return []
        if from_cell == to_cell:
            return [to_cell]
        if self._is_line_of_sight(from_cell, to_cell):
            return [from_cell, to_cell]

        came_from = self._uniform_cost_search(
            from_cell,
            to_cell,
        )

        # Construct cell path starting at `to_cell` and retracing to `start_cell`...
        path_from_goal = [to_cell]
        current_cell = to_cell

        while current_cell is not from_cell:
            came_from_location = came_from.get(current_cell)
            if came_from_location is None:
                return []
            current_cell = came_from_location
            path_from_goal.append(current_cell)

        path = list(reversed(path_from_goal))

        return self._simplify_path(path)

    def _uniform_cost_search(
        self,
        start_cell: GridRef,
        goal_cell: GridRef,
    ) -> dict[GridRef, GridRef | None]:
        came_from: dict[GridRef, GridRef | None] = {start_cell: None}
        cost_so_far: dict[GridRef, float] = {start_cell: 0}
        frontier: PriorityQueue = PriorityQueue()
        frontier.put(0, start_cell)

        while not frontier.is_empty:
            current_cell = frontier.get()

            if current_cell == goal_cell:  # early exit
                break

            for new_cell in self.reachable_neighbours(current_cell):
                new_cost = cost_so_far[current_cell] + self._cost(
                    current_cell, new_cell
                )
                if (
                    new_cell not in came_from or new_cost < cost_so_far[new_cell]
                    # add new_cell to frontier if cheaper
                ):
                    cost_so_far[new_cell] = new_cost
                    frontier.put(priority=new_cost, location=new_cell)
                    came_from[new_cell] = current_cell
        return came_from

    @staticmethod
    def _cost(from_cell: GridRef, to_cell: GridRef) -> float:
        """Calculate the cost as Euclidean distance from one cell to another.

        NB: when calculating next step in a search, locations will be adjacent, so a
        cardinal move has basic cost = 1, and diagonal basic cost =~ 1.4.
        This function is generalised for wider use.

        """
        x_dist = abs(from_cell.x - to_cell.x)
        y_dist = abs(from_cell.y - to_cell.y)
        return math.sqrt(x_dist**2 + y_dist**2)

    def _is_line_of_sight(self, cell_0: GridRef, cell_1: GridRef) -> bool:
        """Determine whether there is line-of-sight between two cells."""
        cells = self._cells_on_line(cell_0, cell_1)
        return all(cell not in self.untraversable_cells for cell in cells)

    def _cells_on_line(self, cell_0: GridRef, cell_1: GridRef) -> set[GridRef]:
        """Return cells on the line between two cells, including end cells."""
        if not self._cell_is_in_bounds(cell_0):
            err_msg = f"Cell {cell_0} is out of bounds."
            raise IndexError(err_msg)
        if not self._cell_is_in_bounds(cell_1):
            err_msg = f"Cell {cell_1} is out of bounds."
            raise IndexError(err_msg)
        if cell_0 == cell_1:
            return {cell_0}

        diagonal_distance = Grid._diagonal_distance(cell_0, cell_1)

        cells = set()
        for step in range(diagonal_distance + 1):
            t = step / diagonal_distance
            point = Grid._lerp_grid_ref(cell_0, cell_1, t)
            cells.add(GridRef(int(point[0]), int(point[1])))
        return cells

    @staticmethod
    def _diagonal_distance(cell_0: GridRef, cell_1: GridRef) -> int:
        """Return the diagonal distance between two cells."""
        delta = cell_1 - cell_0
        return int(max(abs(delta.x), abs(delta.y)))

    @staticmethod
    def _lerp_grid_ref(
        cell_0: GridRef, cell_1: GridRef, t: float
    ) -> tuple[float, float]:
        return lerp(cell_0.x, cell_1.x, t), lerp(cell_0.y, cell_1.y, t)

    def _simplify_path(self, path: list[GridRef]) -> list[GridRef]:
        """Simplify a path by removing redundant points."""
        log_msg = f"Calculated path: {len(path)} points."
        logging.info(log_msg)
        path = self._cull_path(path)
        return self._cull_path(path, reverse=True)

    def _cull_path(
        self, path: list[GridRef], *, reverse: bool = False
    ) -> list[GridRef]:
        """Remove leading points with line-of-sight from first point (or trailing
        points with line-of-sight to last point if `reverse=True`).

        Preserves first and last points.

        """
        min_path_length = 3
        if not path or len(path) <= min_path_length:
            return path

        if reverse:
            index = -2
            while self._is_line_of_sight(path[-1], path[index]) and index > -len(path):
                index -= 1
            culled_path = path[: index + 2] + [path[-1]]
            # should be `path[:index]` but extra point avoids collision issues.
            log_msg = f"- Culled trailing points -> {len(culled_path)} points."
        else:
            index = 1
            while self._is_line_of_sight(path[0], path[index]) and index < len(path):
                index += 1
            culled_path = [path[0]] + path[index - 1 :]
            # should be `path[index:]` but extra point avoids collision issues.
            log_msg = f"- Culled leading points -> {len(culled_path)} points."
        logging.info(log_msg)
        return culled_path
