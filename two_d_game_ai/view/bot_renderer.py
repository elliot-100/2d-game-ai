"""Contains `BotRenderer` class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view import colors
from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pygame import Color


@dataclass(kw_only=True, eq=False)
class BotRenderer(GenericEntityRenderer):
    """Renders a `Bot` to a `WorldRenderer`."""

    def __post_init__(self) -> None:
        super().__post_init__()

    def render(
        self, *, debug_render_mode: bool = False, show_debug_vision: bool = False
    ) -> None:
        """Draws `Bot` and decorations."""
        super().render()
        if not isinstance(self.entity, Bot):
            raise TypeError

        self._draw_icon()

        if debug_render_mode:
            if self.entity.destination:
                self._draw_destination()
            if self.entity.route:
                self._draw_route()
            if show_debug_vision:
                self._draw_vision_cone()
                self._draw_lines_to_others(
                    self.entity.visible_bots, colors.BOT_CAN_SEE_LINE, 3
                )
                self._draw_lines_to_others(
                    self.entity.remembered_bots, colors.BOT_KNOWS_LINE, 1
                )

    def _draw_destination(self) -> None:
        """Draw `Bot` destination icon."""
        if not isinstance(self.entity, Bot):
            raise TypeError

        if not self.entity.destination:
            return

        # Destination marker (X)
        # TypeGuard
        if not self.radius:
            raise TypeError

        offset = self.radius / self.parent.scale_factor
        self.parent.draw_line(
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(-offset, -offset),
            end_pos=self.entity.destination + Vector2(offset, offset),
        )
        self.parent.draw_line(
            color=colors.BOT_DESTINATION_LINE,
            start_pos=self.entity.destination + Vector2(offset, -offset),
            end_pos=self.entity.destination + Vector2(-offset, offset),
        )

    def _draw_route(self) -> None:
        if not isinstance(self.entity, Bot):
            raise TypeError

        if self.entity.route:
            for waypoint in self.entity.route:
                self.parent.draw_circle(
                    surface=self.parent.surface,
                    color=colors.BOT_ROUTE_LINE,
                    center=waypoint,
                    radius=2,
                    width=1,
                    scale_radius=False,
                )

            points = [self.entity.position]
            points.extend(self.entity.route)
            self.parent.draw_polyline(color=colors.BOT_ROUTE_LINE, points=points)

    def _draw_vision_cone(self) -> None:
        """Draw `Bot` vision cone."""
        if not isinstance(self.entity, Bot):
            raise TypeError

        self.parent.draw_pie(
            color=colors.BOT_CAN_SEE_LINE,
            center=self.entity.position,
            radius=self.entity.vision_range,
            central_angle=self.entity.heading.degrees,
            theta=self.entity.VISION_CONE_ANGLE,
        )

    def _draw_lines_to_others(
        self, bots: Iterable[Bot], color: Color, width: int
    ) -> None:
        """Draw lines from Bot to other bots based on visibility or knowledge."""
        for bot in bots:
            self.parent.draw_line(
                color=color,
                start_pos=self.entity.position,
                end_pos=bot.position,
                width=width,
            )

    def _draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        if not isinstance(self.entity, Bot) or not self.radius:
            raise TypeError

        fill_color = colors.SELECTED_FILL if self.is_selected else colors.BOT_FILL
        self.parent.draw_circle(
            surface=self.parent.surface,
            color=fill_color,
            center=self.entity.position,
            radius=self.radius,
        )

        # Heading indicator (line from centre to 'nose')
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        nose_offset = Vector2(0, self.radius).rotate(-self.entity.heading.degrees)
        self.parent.draw_line(
            color=colors.BOT_HEADING_INDICATOR_LINE,
            start_pos=self.entity.position,
            end_pos=self.entity.position + nose_offset,
            width=3,
        )
