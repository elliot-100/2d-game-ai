"""Contains `GenericEntityRenderer` class."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from pygame import Font, Vector2

from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.view import FONT_SIZE, colors

if TYPE_CHECKING:
    from two_d_game_ai.entities.generic_entity import GenericEntity
    from two_d_game_ai.view.world_renderer import WorldRenderer


_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class GenericEntityRenderer(ABC):
    """Renders an entity to a `WorldRenderer`."""

    LABEL_OFFSET: ClassVar = (10, 10)
    """Display units."""

    entity: GenericEntity
    parent: WorldRenderer
    """Parent renderer."""
    is_selected: bool = field(init=False)
    clickable_radius: float = 0
    id: int = field(init=False)
    """Used as hash value."""
    font: Font = field(init=False)

    def __post_init__(self) -> None:
        self.id = len(self.parent.entity_renderers)
        self.font = Font(size=FONT_SIZE)
        self.is_selected = False
        log_msg = f"GenericEntityRenderer initialised for '{self.entity.name}'."
        _logger.debug(log_msg)

    def __hash__(self) -> int:
        return self.id

    @property
    def _pos_v(self) -> Vector2:
        """Get position in window coordinates."""
        return self.parent.to_local(self.entity.position)

    @abstractmethod
    def render(self) -> None:
        """Draw the entity name label to surface."""
        label = self.font.render(
            text=str(self.entity.name),
            antialias=True,
            color=colors.WINDOW_TEXT,
        )
        self.parent.blit(
            source=label,
            dest=self.entity.position,
            display_offset=Vector2(self.LABEL_OFFSET),
        )

    def is_clicked(self, click_pos: Vector2) -> bool:
        """Determine if the entity is clicked on.

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
