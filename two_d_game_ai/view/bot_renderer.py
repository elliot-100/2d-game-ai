"""Module containing `BotRenderer` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer
from two_d_game_ai.view.primitives import (
    draw_scaled_circle,
    draw_scaled_circular_arc,
    draw_scaled_line,
)

if TYPE_CHECKING:
    from pygame import Color


class BotRenderer(GenericEntityRenderer):
    """Renders a Bot to a Surface."""

    ICON_RADIUS: ClassVar[int] = 10
    """Display units."""

    def draw(self) -> None:
        """Draws the Bot and decorations to the surface."""
        super().draw()
        if not isinstance(self.entity, Bot):
            raise TypeError
        if self.entity.destination is not None:
            self._draw_destination()
            self._draw_route()
        self._draw_vision_cone()
        self._draw_lines_to_others(self.entity.visible_bots, colors.BOT_CAN_SEE_LINE, 4)
        self._draw_lines_to_others(self.entity.known_bots, colors.BOT_KNOWS_LINE, 1)
        self._draw_icon()
        self.clickable_radius = self.ICON_RADIUS

    def _draw_destination(self) -> None:
        """Draw Bot destination icon, and line to it."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        if not self.entity.destination:
            return  # Guard clause

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.view.scale_factor
        draw_scaled_line(
            self.view,
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(-offset, -offset),
            end_pos=self.entity.destination + Vector2(offset, offset),
        )
        draw_scaled_line(
            self.view,
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(offset, -offset),
            end_pos=self.entity.destination + Vector2(-offset, offset),
        )

        # Line from Bot centre to destination
        draw_scaled_line(
            self.view,
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.pos,
            end_pos=self.entity.destination,
        )

    def _draw_route(self) -> None:
        if not isinstance(self.entity, Bot):
            raise TypeError
        for i in range(len(self.entity.route)):
            draw_scaled_circle(
                self.view,
                color=colors.BOT_ROUTE_LINE,
                center=self.entity.route[i],
                radius=self.ICON_RADIUS / 4,
                scale_radius=False,
            )

    def _draw_vision_cone(self) -> None:
        """Draw Bot vision cone to surface."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        vision_start_angle = (
            self.entity.heading.degrees - self.entity.VISION_CONE_ANGLE / 2
        )
        vision_end_angle = (
            self.entity.heading.degrees + self.entity.VISION_CONE_ANGLE / 2
        )
        vision_limit_offset = Vector2(0, self.ICON_RADIUS * 2)

        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        start_wedge_point = self.entity.pos + vision_limit_offset.rotate(
            -vision_start_angle
        )
        end_wedge_point = self.entity.pos + vision_limit_offset.rotate(
            -vision_end_angle
        )

        draw_scaled_line(
            self.view,
            color=colors.BOT_CAN_SEE_LINE,
            start_pos=self.entity.pos,
            end_pos=start_wedge_point,
        )
        draw_scaled_line(
            self.view,
            color=colors.BOT_CAN_SEE_LINE,
            start_pos=self.entity.pos,
            end_pos=end_wedge_point,
        )
        draw_scaled_circular_arc(
            self.view,
            color=colors.BOT_CAN_SEE_LINE,
            center=self.entity.pos,
            radius=2 * self.ICON_RADIUS,
            start_angle=vision_start_angle,
            stop_angle=vision_end_angle,
        )

    def _draw_lines_to_others(self, bots: set[Bot], color: Color, width: int) -> None:
        """Draw lines from Bot to other bots based on visibility or knowledge."""
        for bot in bots:
            draw_scaled_line(
                self.view,
                color=color,
                start_pos=self.entity.pos,
                end_pos=bot.pos,
                width=width,
            )

    def _draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        fill_color = colors.SELECTED_FILL if self.is_selected else colors.BOT_FILL
        draw_scaled_circle(
            self.view,
            color=fill_color,
            center=self.entity.pos,
            radius=self.ICON_RADIUS,
            scale_radius=False,
        )

        # Heading indicator (line from centre to 'nose')
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        nose_offset = Vector2(0, self.ICON_RADIUS).rotate(-self.entity.heading.degrees)
        draw_scaled_line(
            self.view,
            color=colors.BOT_HEADING_INDICATOR_LINE,
            start_pos=self.entity.pos,
            end_pos=self.entity.pos + nose_offset / self.view.scale_factor,
            width=3,
        )
