"""MovementBlockRenderer class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.entities import MovementBlock
from two_d_game_ai.geometry.utils import point_in_or_on_circle
from two_d_game_ai.render import colors
from two_d_game_ai.render.generic_entity_renderer import _GenericEntityRenderer
from two_d_game_ai.render.primitives import _scaled_circle

if TYPE_CHECKING:
    from pygame import Font

    from two_d_game_ai import Vector2
    from two_d_game_ai.render.view import View


class MovementBlockRenderer(_GenericEntityRenderer):
    """Renders a Block to a Surface.

    Attributes
    ----------
    clickable_radius: int | float
        Radius in which to register mouse click (display coordinates)
    view:
        The View context
    entity: MovementBlock
        The entity to render
    font: Font
        # TODO
    is_selected: bool
        Whether the rendered entity is selected

    Non-public attributes/properties
    ----------
    _pos_v: Vector2
        Position (display coordinates)
    """

    def __init__(
        self,
        view: View,
        entity: MovementBlock,
        font: Font,
    ) -> None:
        super().__init__(view, entity, font)
        if isinstance(self.entity, MovementBlock):
            self.clickable_radius = self.entity.collision_radius

    def draw(self) -> None:
        """Draws the MovementBlock to the surface."""
        super().draw()  # label only

        if not isinstance(self.entity, MovementBlock):
            raise TypeError

        fill_color = colors.SELECTED if self.is_selected else colors.VOID
        _scaled_circle(
            self.view,
            color=fill_color,
            center=self.entity.pos_v,
            radius=self.entity.collision_radius,
        )

    def is_clicked(self, click_pos: Vector2) -> bool:
        """Determine if the clicked location is on the entity icon.

        Parameters
        ----------
        click_pos
            The position of the click in window coordinates.

        Returns
        -------
        bool
            True if the click position is within or on the icon radius.
        """
        return point_in_or_on_circle(click_pos, self._pos_v, self.clickable_radius)
