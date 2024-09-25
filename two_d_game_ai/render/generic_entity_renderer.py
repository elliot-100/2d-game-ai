"""Module containing `_GenericEntityRenderer` class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.render import colors
from two_d_game_ai.render.primitives import draw_scaled_blit

if TYPE_CHECKING:
    from pygame import Font, Vector2

    from two_d_game_ai.entities.generic_entity import GenericEntity
    from two_d_game_ai.render.view import View


class _GenericEntityRenderer(ABC):
    """Renders an entity to a Surface."""

    LABEL_OFFSET = (10, 10)
    """Display units."""

    def __init__(self, view: View, entity: GenericEntity, font: Font) -> None:
        self.view = view
        self.entity = entity
        self.font = font
        self.is_selected = False
        self.clickable_radius: float = 0

    @property
    def _pos_v(self) -> Vector2:
        """Get position in window coordinates."""
        return self.view.to_display(self.entity.pos_v)

    @abstractmethod
    def draw(self) -> None:
        """Draw the entity to the surface."""
        self._draw_label()

    def _draw_label(self) -> None:
        """Draw entity name label to surface."""
        label = self.font.render(
            text=str(self.entity.name),
            antialias=True,
            color=colors.WINDOW_TEXT,
        )
        draw_scaled_blit(
            self.view,
            source=label,
            dest=self.entity.pos_v,
            display_offset=self.LABEL_OFFSET,
        )

    def is_clicked(self, click_pos: Vector2) -> bool:
        """Determine if the entity is clicked.

        Parameters
        ----------
        click_pos
            The position of the click in window coordinates.

        Returns
        -------
        bool
            True if the click position is within or on the clickable radius.
        """
        return point_in_or_on_circle(click_pos, self._pos_v, self.clickable_radius)
