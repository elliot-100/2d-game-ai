"""Contains `Grid` class."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2
from pygame.math import lerp

from two_d_game_ai.world.grid_ref import GridRef
from two_d_game_ai.world.priority_queue import PriorityQueue

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.world import World


_MIN_PATH_NODES: int = 3

_logger = logging.getLogger(__name__)


@dataclass
class Grid:
    """Grid class.

    NB: there is no 'Grid cell' class.

    """

    DEFAULT_SIZE: ClassVar = 2

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
    size: int = DEFAULT_SIZE
    """`Grid` units per side."""
    offset: GridRef = field(init=False)
    movement_blocking_cells: set[GridRef] = field(init=False, default_factory=set)
    vision_blocking_cells: set[GridRef] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        _offset = -self.size // 2
        self.offset = GridRef(_offset, _offset)
        log_msg = f"{self} initialised."
        _logger.info(log_msg)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.size=})"

    @property
    def cells(self) -> set[GridRef]:
        """Return all cells."""
        return {
            GridRef(x, y) + self.offset
            for x in range(self.size)
            for y in range(self.size)
        }

    def _cell_is_in_bounds(self, cell: GridRef) -> bool:
        """Determine whether a cell is within the `Grid`."""
        return abs(cell.x) <= self.size and abs(cell.y) <= self.size

    def reachable_neighbours(self, cell: GridRef) -> set[GridRef]:
        """Return a cell's reachable (by movement) neighbours."""
        reachable_neighbours: set[GridRef] = set()

        if cell in self.movement_blocking_cells:
            return set()

        for dir_ in self._DIRECTIONS:
            neighbour = GridRef(cell.x + dir_[0], cell.y + dir_[1])
            if (
                self._cell_is_in_bounds(neighbour)
                and neighbour not in self.movement_blocking_cells
            ):
                reachable_neighbours.add(neighbour)

        return reachable_neighbours

    def route(
        self,
        from_cell: GridRef,
        to_cell: GridRef,
    ) -> list[GridRef] | None:
        """Determine a cell-based route between two cells.

        Returns
        -------
        `list[GridRef]`
            Cells on the path to `to_cell`, including `to_cell` itself.
        `None`
            if no path found.
        """
        # Early return cases:
        if (
            from_cell in self.movement_blocking_cells
            or to_cell in self.movement_blocking_cells
        ):
            return None
        if from_cell == to_cell:
            return [to_cell]
        if self.is_line_of_movement(from_cell, to_cell):
            return [from_cell, to_cell]

        came_from = self._uniform_cost_search(from_cell, to_cell)

        # Construct cell path starting at `to_cell` and retracing to `start_cell`...
        path_from_goal = [to_cell]
        current_cell = to_cell

        while current_cell != from_cell:
            came_from_location = came_from.get(current_cell)
            if came_from_location is None:
                log_msg = "No route!"
                _logger.debug(log_msg)
                return None
            current_cell = came_from_location
            path_from_goal.append(current_cell)

        log_msg = f"Calculated path: {len(path_from_goal)} points."
        _logger.debug(log_msg)

        simplified_path = self.cull_path_line_of_sight(path=path_from_goal)
        simplified_path = self.cull_path_line_of_sight(
            path=simplified_path, reverse=True
        )
        return self.cull_path_collinear_nodes(simplified_path)

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

    def is_line_of_sight(self, cell_0: GridRef, cell_1: GridRef) -> bool:
        """Determine whether there is line-of-sight (i.e. no vision-blocking cells)
        between two cells.
        """
        cells = self._cells_on_line(cell_0, cell_1)
        return all(cell not in self.vision_blocking_cells for cell in cells)

    def is_line_of_movement(self, cell_0: GridRef, cell_1: GridRef) -> bool:
        """Determine whether there is line-of-movement (i.e. no movement-blocking cells)
        between two cells.
        """
        cells = self._cells_on_line(cell_0, cell_1)
        return all(cell not in self.movement_blocking_cells for cell in cells)

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
            point = Grid._lerp_grid_ref(cell_0, cell_1, step / diagonal_distance)
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

    def cull_path_line_of_sight(
        self, *, path: Sequence[GridRef], reverse: bool = False
    ) -> list[GridRef]:
        """Remove nodes that have line-of-sight from the first node, or last node if
        `reversed` is `True`.
        """
        if not path or len(path) <= _MIN_PATH_NODES:
            return list(path)

        log_end = "goal"

        if reverse:
            path = list(reversed(path))
            log_end = "start"

        culled_path = [path[0]]
        for i in range(len(path) - 1):
            if not self.is_line_of_movement(culled_path[0], path[i + 1]):
                culled_path.extend(path[i:])
                break

        log_msg = f"After culling from {log_end}: {len(culled_path)} points."
        _logger.debug(log_msg)

        return culled_path

    @staticmethod
    def cull_path_collinear_nodes(path: list[GridRef]) -> list[GridRef]:
        """Remove adjacent collinear nodes from `path`."""
        if not path or len(path) <= _MIN_PATH_NODES:
            return list(path)

        culled_path = path[:2]
        for node in path[2:]:
            if not Grid._grid_refs_are_collinear(
                culled_path[-2], culled_path[-1], node
            ):
                culled_path.append(node)

        log_msg = f"After culling adjacent collinear: {len(culled_path)} points."
        _logger.debug(log_msg)

        return culled_path

    @staticmethod
    def _grid_refs_are_collinear(gr0: GridRef, gr1: GridRef, gr2: GridRef) -> bool:
        dx1 = gr1.x - gr0.x
        dy1 = gr1.y - gr0.y
        dx2 = gr2.x - gr1.x
        dy2 = gr2.y - gr1.y
        return dx1 * dy2 == dy1 * dx2

    @staticmethod
    def grid_ref_from_world_pos(world: World, pos: Vector2) -> GridRef:
        """Return the `GridRef` of the cell containing `World` position."""
        return GridRef(
            int(pos.x // world.grid_resolution), int(pos.y // world.grid_resolution)
        )

    @staticmethod
    def cell_centre_to_world_pos(grid_ref: GridRef, world: World) -> Vector2:
        """Return the `World` position of the centre of the cell."""
        return Vector2(
            grid_ref.x * world.grid_resolution,
            grid_ref.y * world.grid_resolution,
        ) + Vector2(world.grid_resolution / 2)
