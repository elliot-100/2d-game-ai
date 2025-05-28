"""TO DO."""

from collections.abc import Iterable

from two_d_game_ai.world.grid import Grid
from two_d_game_ai.world.grid_ref import GridRef

EMPTY = "·"
HIGHLIGHT = "X"


def as_text(grid: Grid, highlight: Iterable[GridRef]) -> str:
    """TO DO."""
    header = "0,0"
    data_lines = []
    for x in range(grid.size):
        line = "".join(
            f"{HIGHLIGHT} " if GridRef(x, y) in highlight else f"{EMPTY} "
            for y in range(grid.size)
        )
        data_lines.append(line)
    return header + "\n" + "\n".join(data_lines)


g = Grid(size=5)
s = as_text(g, highlight=[GridRef(x=3, y=3), GridRef(x=2, y=2)])
