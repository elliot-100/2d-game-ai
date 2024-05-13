"""BotRenderer class: responsible for rendering a Bot and decorations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from two_d_game_ai import Vector2
from two_d_game_ai.entities import Bot
from two_d_game_ai.render import colors
from two_d_game_ai.render.generic_entity_renderer import GenericEntityRenderer
from two_d_game_ai.render.primitives import _circle, _scaled_circular_arc, _scaled_line

if TYPE_CHECKING:
    from pygame import Color


class BotRenderer(GenericEntityRenderer):
    """Renders a Bot to a Surface.

    Provides methods to draw Bot icon and related elements.

    Attributes
    ----------
    entity: Bot
        The entity to render
    font: Font
        # TODO
    is_selected: bool
        Whether the rendered bot is selected
    view:
        The View context

    Non-public attributes/properties
    ----------
    _pos_v: Vector2
        Position (display coordinates)
    """

    def draw(self) -> None:
        """Draws the Bot and decorations to the surface."""
        super().draw()
        if not isinstance(self.entity, Bot):
            raise TypeError
        if self.entity.destination_v is not None:
            self._draw_destination()
        self._draw_vision_cone()
        self._draw_lines_to_others(self.entity.visible_bots, colors.VISION, 4)
        self._draw_lines_to_others(self.entity.known_bots, colors.KNOWS, 1)
        self._draw_icon()

    def _draw_destination(self) -> None:
        """Draw Bot destination icon, and line to it."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        if not self.entity.destination_v:
            return  # Guard clause

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.view.scale_factor
        _scaled_line(
            self.view,
            color=colors.FOREGROUND,
            start_pos=self.entity.destination_v + Vector2(-offset, -offset),
            end_pos=self.entity.destination_v + Vector2(offset, offset),
        )
        _scaled_line(
            self.view,
            color=colors.FOREGROUND,
            start_pos=self.entity.destination_v + Vector2(offset, -offset),
            end_pos=self.entity.destination_v + Vector2(-offset, offset),
        )

        # Line from Bot centre to destination
        _scaled_line(
            self.view,
            color=colors.FOREGROUND,
            start_pos=self.entity.pos_v,
            end_pos=self.entity.destination_v,
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
        vision_limit_offset = Vector2(0, 10)

        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        start_wedge_point = self.entity.pos_v + vision_limit_offset.rotate(
            -vision_start_angle
        )
        end_wedge_point = self.entity.pos_v + vision_limit_offset.rotate(
            -vision_end_angle
        )

        _scaled_line(
            self.view,
            color=colors.VISION,
            start_pos=self.entity.pos_v,
            end_pos=start_wedge_point,
        )
        _scaled_line(
            self.view,
            color=colors.VISION,
            start_pos=self.entity.pos_v,
            end_pos=end_wedge_point,
        )
        _scaled_circular_arc(
            self.view,
            color=colors.VISION,
            center=self.entity.pos_v,
            radius=10,
            start_angle=vision_start_angle,
            stop_angle=vision_end_angle,
        )

    def _draw_lines_to_others(self, bots: set[Bot], color: Color, width: int) -> None:
        """Draw lines from Bot to other bots based on visibility or knowledge."""
        for bot in bots:
            _scaled_line(
                self.view,
                color=color,
                start_pos=self.entity.pos_v,
                end_pos=bot.pos_v,
                width=width,
            )

    def _draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        if not isinstance(self.entity, Bot):
            raise TypeError
        fill_color = colors.SELECTED if self.is_selected else colors.FOREGROUND
        _circle(
            self.view,
            color=fill_color,
            center=self._pos_v,
            radius=self.ICON_RADIUS,
        )

        # Heading indicator (line from centre to 'nose')
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        nose_offset = Vector2(0, self.ICON_RADIUS).rotate(-self.entity.heading.degrees)
        _scaled_line(
            self.view,
            color=colors.BACKGROUND,
            start_pos=self.entity.pos_v,
            end_pos=self.entity.pos_v + nose_offset / self.view.scale_factor,
            width=3,
        )
