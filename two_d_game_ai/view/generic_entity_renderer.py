"""Contains generic entity renderer classes."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2

from two_d_game_ai.geometry import point_in_or_on_circle, point_in_or_on_rect
from two_d_game_ai.view import colors

if TYPE_CHECKING:
    from two_d_game_ai.entities.generic_entities import GenericEntity
    from two_d_game_ai.view.world_renderer import WorldRenderer


_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class GenericEntityRenderer(ABC):
    """Renders an entity to a `WorldRenderer`."""

    LABEL_OFFSET: ClassVar = (10, 10)
    """Display units."""

    id: int = field(init=False)
    """Used as hash value."""
    entity: GenericEntity
    parent: WorldRenderer
    """Parent renderer."""
    is_selected: bool = field(init=False)
    radius: None | float = field(init=False)
    size: None | Vector2 = None

    def __post_init__(self) -> None:
        if hasattr(self.entity, "radius"):
            self.radius = self.entity.radius
        self.id = len(self.parent.entity_renderers)
        self.is_selected = False
        log_msg = f"{self.description} initialised for {self.entity.description}."
        _logger.info(log_msg)

    def __hash__(self) -> int:
        return self.id

    @property
    def description(self) -> str:
        """Description of entity."""
        return f"{type(self).__name__}"

    @abstractmethod
    def render(self) -> None:
        """Draw the entity name label to surface."""
        label = self.parent.font.render(
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
            True if the click position is within or on the renderer.
        """
        click_pos_world = self.parent.to_world(click_pos)

        if hasattr(self.entity, "radius"):
            return point_in_or_on_circle(
                point=click_pos_world,
                circle_centre=self.entity.position,
                circle_radius=self.entity.radius,
            )
        if hasattr(self.entity, "size"):
            return point_in_or_on_rect(
                point=click_pos_world,
                rect_min=self.entity.position,
                rect_size=self.entity.size,
            )
        return False
