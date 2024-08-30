"""Module containing `_GenericEntityRenderer` class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from two_d_game_ai.render import colors
from two_d_game_ai.render.primitives import draw_scaled_blit

if TYPE_CHECKING:
    from pygame import Font

    from two_d_game_ai import Vector2
    from two_d_game_ai.entities.generic_entity import _GenericEntity
    from two_d_game_ai.render.view import View


class _GenericEntityRenderer(ABC):
    """Renders an entity to a Surface.

    Attributes
    ----------
    clickable_radius
        Radius in which to register mouse click (display coordinates)
    entity
        The entity to render
    font
        # TODO
    is_selected
        Whether the rendered entity is selected
    view
        The View context

    Non-public attributes/properties
    ----------
    _pos_v
        Position (display coordinates)

    """

    LABEL_OFFSET = (10, 10)
    """Display units."""

    def __init__(self, view: View, entity: _GenericEntity, font: Font) -> None:
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
            color=colors.LABEL,
        )
        draw_scaled_blit(
            self.view,
            source=label,
            dest=self.entity.pos_v,
            display_offset=self.LABEL_OFFSET,
        )
