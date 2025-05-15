"""Contains `Obstacle` renderer classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from pygame import FRect

from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer


@dataclass(kw_only=True, eq=False)
class ObstacleRenderer(GenericEntityRenderer):
    """Renders an obstacle to a `WorldRenderer`."""

    LABEL_OFFSET: ClassVar = (0, 0)
    """Display units."""

    def __post_init__(self) -> None:
        super().__post_init__()

    def render(self) -> None:
        """Draw the outline of the obstacle."""
        super().render()  # label only

        color = colors.DEBUG if self.is_selected else colors.OBSTACLE_LINE
        if isinstance(self.entity, ObstacleCircle):
            self.parent.draw_circle(
                surface=self.parent.surface,
                color=color,
                center=self.entity.position,
                radius=self.entity.radius,
                width=1,
            )
        elif isinstance(self.entity, ObstacleRectangle):
            self.parent.draw_rect(
                color=color,
                rect=FRect(
                    self.entity.position,
                    self.entity.size,
                ),
                width=1,
            )
