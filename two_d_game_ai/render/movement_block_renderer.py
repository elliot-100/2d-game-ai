"""Module containing `MovementBlockRenderer` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.entities import MovementBlock
from two_d_game_ai.render import colors
from two_d_game_ai.render.generic_entity_renderer import _GenericEntityRenderer
from two_d_game_ai.render.primitives import draw_scaled_circle

if TYPE_CHECKING:
    from pygame import Font

    from two_d_game_ai.render.view import View


class MovementBlockRenderer(_GenericEntityRenderer):
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

        fill_color = colors.SELECTED_FILL if self.is_selected else colors.WINDOW_FILL
        draw_scaled_circle(
            self.view,
            color=fill_color,
            center=self.entity.pos,
            radius=self.entity.radius,
        )
