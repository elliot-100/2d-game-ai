"""GenericEntityRenderer class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai.geometry.utils import point_in_or_on_circle
from two_d_game_ai.render import colors
from two_d_game_ai.render.primitives import _scaled_blit

if TYPE_CHECKING:
    from pygame import Font

    from two_d_game_ai import Vector2
    from two_d_game_ai.entities import Bot
    from two_d_game_ai.render.view import View


class GenericEntityRenderer:
    """Renders an entity to a Surface.

    Attributes
    ----------
    view:
        The View context
    entity: Bot
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

    ICON_RADIUS = 10  # in pixels
    LABEL_OFFSET = (10, 10)  # in pixels

    def __init__(self, view: View, entity: Bot, font: Font) -> None:
        self.view = view
        self.entity = entity
        self.font = font
        self.is_selected = False

    @property
    def _pos_v(self) -> Vector2:
        """Get position in window coordinates."""
        return self.view.to_display(self.entity.pos_v)

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
        return point_in_or_on_circle(click_pos, self._pos_v, self.ICON_RADIUS)

    def draw(self) -> None:
        """Draw the entity to the surface."""
        self._draw_label()

    def _draw_label(self) -> None:
        """Draw entity name label to surface."""
        label = self.font.render(
            text=str(self.entity.name),
            antialias=True,
            color=colors.LABEL,
        )
        _scaled_blit(
            self.view,
            source=label,
            dest=self.entity.pos_v,
            display_offset=self.LABEL_OFFSET,
        )
