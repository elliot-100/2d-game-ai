"""Contains `BotRenderer` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pygame import Color

logger = logging.getLogger(__name__)


@dataclass
class BotRenderer(GenericEntityRenderer):
    """Renders a `Bot` to a `WorldRenderer`."""

    ICON_RADIUS: ClassVar[int] = 10
    """Display units."""

    def __post_init__(self) -> None:
        super().__post_init__()
        log_msg = f"BotRenderer initialised for '{self.entity.name}'."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return super().__hash__()

    def draw(self, *, debug_render_mode: bool = False) -> None:
        """Draws `Bot` and decorations."""
        super().draw()
        if not isinstance(self.entity, Bot):
            raise TypeError

        if debug_render_mode:
            if self.entity.destination:
                self._draw_destination()
            if self.entity.route:
                self._draw_route()
            self._draw_vision_cone()
            self._draw_lines_to_others(
                self.entity.visible_bots, colors.BOT_CAN_SEE_LINE, 3
            )
            self._draw_lines_to_others(
                self.entity.remembered_bots, colors.BOT_KNOWS_LINE, 1
            )
        self._draw_icon()
        self.clickable_radius = self.ICON_RADIUS

    def _draw_destination(self) -> None:
        """Draw `Bot` destination icon, and line to it."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        if not self.entity.destination:
            return  # Guard clause

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.world_renderer.scale_factor
        self.world_renderer.draw_line(
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(-offset, -offset),
            end_pos=self.entity.destination + Vector2(offset, offset),
        )
        self.world_renderer.draw_line(
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(offset, -offset),
            end_pos=self.entity.destination + Vector2(-offset, offset),
        )

        # Line from Bot centre to destination
        self.world_renderer.draw_line(
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.position,
            end_pos=self.entity.destination,
        )

    def _draw_route(self) -> None:
        min_path_nodes: int = 2

        if not isinstance(self.entity, Bot):
            raise TypeError

        for i in range(len(self.entity.route)):
            self.world_renderer.draw_circle(
                color=colors.BOT_ROUTE_LINE,
                center=self.entity.route[i],
                radius=2,
                width=1,
                scale_radius=False,
            )
        if len(self.entity.route) >= min_path_nodes:
            self.world_renderer.draw_poly(
                color=colors.BOT_ROUTE_LINE,
                points=[self.entity.position, *self.entity.route],
            )

    def _draw_vision_cone(self) -> None:
        """Draw `Bot` vision cone."""
        angle_step_degrees: int = 10

        if not isinstance(self.entity, Bot):
            raise TypeError

        vision_limit_offset = Vector2(0, self.ICON_RADIUS * 2)

        draw_angles = [
            *list(range(0, int(self.entity.VISION_CONE_ANGLE), angle_step_degrees)),
            self.entity.VISION_CONE_ANGLE,
        ]
        # include the last angle so it's always drawn, irrespective of
        # `angle_step_degrees`

        offsets = [
            # NB legacy use of Pygame CCW rotation here, thus negative angle:
            vision_limit_offset.rotate(
                self.entity.VISION_CONE_ANGLE / 2 - self.entity.heading.degrees - angle
            )
            for angle in draw_angles
        ]
        self.world_renderer.draw_poly(
            color=colors.BOT_CAN_SEE_LINE,
            closed=True,
            points=[self.entity.position]
            + [self.entity.position + offset for offset in offsets],
        )

    def _draw_lines_to_others(
        self, bots: Iterable[Bot], color: Color, width: int
    ) -> None:
        """Draw lines from Bot to other bots based on visibility or knowledge."""
        for bot in bots:
            self.world_renderer.draw_line(
                color=color,
                start_pos=self.entity.position,
                end_pos=bot.position,
                width=width,
            )

    def _draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        fill_color = colors.SELECTED_FILL if self.is_selected else colors.BOT_FILL
        self.world_renderer.draw_circle(
            color=fill_color,
            center=self.entity.position,
            radius=self.ICON_RADIUS,
            scale_radius=False,
        )

        # Heading indicator (line from centre to 'nose')
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        nose_offset = Vector2(0, self.ICON_RADIUS).rotate(-self.entity.heading.degrees)
        self.world_renderer.draw_line(
            color=colors.BOT_HEADING_INDICATOR_LINE,
            start_pos=self.entity.position,
            end_pos=self.entity.position
            + nose_offset / self.world_renderer.scale_factor,
            width=3,
        )
