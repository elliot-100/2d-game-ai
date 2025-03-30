"""Contains `ObstacleRenderer` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from two_d_game_ai.entities.obstacle import Obstacle
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer


@dataclass(kw_only=True, eq=False)
class ObstacleRenderer(GenericEntityRenderer):
    """Renders the outline of `Obstacle` to a `WorldRenderer`.

    Fill is currently handled on a `Grid` basis by
    `WorldRenderer.render_obstructed_cells()`.
    """

    LABEL_OFFSET: ClassVar = (0, 0)
    """Display units."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if isinstance(self.entity, Obstacle):
            self.clickable_radius = self.entity.radius

    def render(self) -> None:
        """Draw the `Obstacle`."""
        super().render()  # label only

        if not isinstance(self.entity, Obstacle):
            raise TypeError

        color = colors.DEBUG if self.is_selected else colors.MOVEMENT_BLOCK_LINE
        self.parent.draw_circle(
            surface=self.parent.surface,
            color=color,
            center=self.entity.position,
            radius=self.entity.radius,
            width=1,
        )
