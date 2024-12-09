"""Module containing `MovementBlockRenderer` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer

if TYPE_CHECKING:
    from pygame import Font

    from two_d_game_ai.view.view import View


class MovementBlockRenderer(GenericEntityRenderer):
    """Renders a Block to a Surface."""

    def __init__(
        self,
        view: View,
        entity: MovementBlock,
        font: Font,
    ) -> None:
        super().__init__(view, entity, font)
        if isinstance(self.entity, MovementBlock):
            self.clickable_radius = self.entity.radius

    def draw(self) -> None:
        """Draws the MovementBlock to the surface."""
        super().draw()  # label only

        if not isinstance(self.entity, MovementBlock):
            raise TypeError

        color = colors.DEBUG if self.is_selected else colors.MOVEMENT_BLOCK_LINE
        self.view.draw_circle(
            color=color,
            center=self.entity.pos,
            radius=self.entity.radius,
            width=2,
        )
