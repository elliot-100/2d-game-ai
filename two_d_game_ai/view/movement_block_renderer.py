"""Contains `MovementBlockRenderer` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import ClassVar

from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer

logger = logging.getLogger(__name__)


@dataclass
class MovementBlockRenderer(GenericEntityRenderer):
    """Renders a `MovementBlock` to a `WorldRenderer`."""

    LABEL_OFFSET: ClassVar = (0, 0)
    """Display units."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if isinstance(self.entity, MovementBlock):
            self.clickable_radius = self.entity.radius
        log_msg = f"BotRenderer initialised for {self.entity.name}"
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return super().__hash__()

    def draw(self) -> None:
        """Draw the `MovementBlock`."""
        super().draw()  # label only

        if not isinstance(self.entity, MovementBlock):
            raise TypeError

        color = colors.DEBUG if self.is_selected else colors.MOVEMENT_BLOCK_LINE
        self.world_renderer.draw_circle(
            color=color,
            center=self.entity.position,
            radius=self.entity.radius,
            width=1,
        )
