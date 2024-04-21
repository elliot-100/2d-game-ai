"""BotRenderer class: responsible for rendering a Bot and decorations."""

from __future__ import annotations

from math import radians
from typing import TYPE_CHECKING

import pygame
from pygame import Color, Font, Rect, Surface

from two_d_game_ai import Vector2
from two_d_game_ai.geometry.utils import point_in_or_on_circle
from two_d_game_ai.render import colors

if TYPE_CHECKING:
    from two_d_game_ai.entities import Bot
    from two_d_game_ai.render.view import View


class BotRenderer:
    """Renders a Bot to a Surface.

    Provides methods to draw Bot icon and related elements.

    Attributes
    ----------
    view:
        The View context
    bot: Bot
        The Bot to render
    font: Font
        # TODO
    """

    ICON_RADIUS = 10  # in pixels
    LABEL_OFFSET = (10, 10)  # in pixels

    def __init__(
        self,
        *,
        view: View,
        bot: Bot,
        font: Font,
    ) -> None:
        self.view = view
        self.bot = bot
        self.font = font
        self.is_selected = False

    @property
    def pos_v(self) -> Vector2:
        """Get position in window coordinates."""
        return self.view.to_display(self.bot.pos_v)

    def draw(self) -> None:
        """Draws the Bot and decorations to the surface."""
        if self.bot.destination_v:
            self.draw_destination()
        self.draw_vision_cone()
        if self.bot.visible_bots:
            for visible_bot in self.bot.visible_bots:
                self.draw_visible_line(visible_bot)
        if self.bot.known_bots:
            for known_bot in self.bot.known_bots:
                self.draw_known_line(known_bot)
        self.draw_icon()
        self.draw_label()

    def draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        fill_color = colors.SELECTED if self.is_selected else colors.FOREGROUND
        pygame.draw.circle(
            surface=self.view.window,
            color=fill_color,
            center=self.pos_v,
            radius=self.ICON_RADIUS,
        )

        # Heading indicator (line from centre to 'nose')
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        nose_offset = Vector2(0, self.ICON_RADIUS).rotate(-self.bot.heading.degrees)
        self._draw_scaled_line(
            color=colors.BACKGROUND,
            start_pos=self.bot.pos_v,
            end_pos=self.bot.pos_v + nose_offset / self.view.scale_factor,
            width=3,
        )

    def draw_label(self) -> None:
        """Draw Bot name label to surface."""
        label = self.font.render(
            text=self.bot.name,
            antialias=True,
            color=colors.LABEL,
        )
        self._scaled_blit(
            source=label,
            dest=self.bot.pos_v,
            display_offset=self.LABEL_OFFSET,
        )

    def draw_destination(self) -> None:
        """Draw Bot destination icon, and line to it."""
        if not self.bot.destination_v:
            raise TypeError

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.view.scale_factor
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.destination_v + Vector2(-offset, -offset),
            end_pos=self.bot.destination_v + Vector2(offset, offset),
        )
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.destination_v + Vector2(offset, -offset),
            end_pos=self.bot.destination_v + Vector2(-offset, offset),
        )

        # Line from Bot centre to destination
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.pos_v,
            end_pos=self.bot.destination_v,
        )

    def draw_visible_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other visible Bot."""
        self._draw_scaled_line(
            color=colors.VISION,
            start_pos=self.bot.pos_v,
            end_pos=other_bot.pos_v,
            width=4,
        )

    def draw_known_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other known Bot."""
        self._draw_scaled_line(
            color=colors.KNOWS,
            start_pos=self.bot.pos_v,
            end_pos=other_bot.pos_v,
        )

    def draw_vision_cone(self) -> None:
        """Draw Bot vision cone to surface."""
        vision_start_angle = self.bot.heading.degrees - self.bot.VISION_CONE_ANGLE / 2
        vision_end_angle = self.bot.heading.degrees + self.bot.VISION_CONE_ANGLE / 2
        vision_limit_offset = Vector2(0, 10)

        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        start_wedge_point = self.bot.pos_v + vision_limit_offset.rotate(
            -vision_start_angle
        )
        end_wedge_point = self.bot.pos_v + vision_limit_offset.rotate(
            -vision_end_angle
        )

        self._draw_scaled_line(
            color=colors.VISION,
            start_pos=self.bot.pos_v,
            end_pos=start_wedge_point,
        )
        self._draw_scaled_line(
            color=colors.VISION,
            start_pos=self.bot.pos_v,
            end_pos=end_wedge_point,
        )
        self._draw_scaled_circular_arc(
            color=colors.VISION,
            center=self.bot.pos_v,
            start_angle=vision_start_angle,
            stop_angle=vision_end_angle,
            radius=10,
        )

    def _draw_scaled_line(
        self,
        *,
        color: Color,
        start_pos: Vector2,
        end_pos: Vector2,
        width: int = 1,
    ) -> None:
        pygame.draw.line(
            surface=self.view.window,
            color=color,
            start_pos=self.view.to_display(start_pos),
            end_pos=self.view.to_display(end_pos),
            width=width,
        )

    def _draw_scaled_circular_arc(
        self,
        color: Color,
        center: Vector2,
        radius: int,
        start_angle: float,
        stop_angle: float,
        width: int = 1,
    ) -> None:
        """Draw a circular arc, scaled to display coordinates."""
        enclosing_rect_dimension = int(2 * radius * self.view.scale_factor)
        enclosing_rect = Rect(0, 0, enclosing_rect_dimension, enclosing_rect_dimension)
        display_center = self.view.to_display(center)
        # Pygame.Rect requires integer coordinates; draw.arc call does not accept Frect
        enclosing_rect.center = int(display_center.x), int(display_center.y)

        pygame.draw.arc(
            surface=self.view.window,
            color=color,
            rect=enclosing_rect,
            start_angle=_to_display_radians(stop_angle),
            stop_angle=_to_display_radians(start_angle),
            width=width,
        )

    def _scaled_blit(
        self,
        *,
        source: Surface,
        dest: Vector2,
        display_offset: tuple[int, int],
    ) -> None:
        self.view.window.blit(
            source=source,
            dest=self.view.to_display(dest) + display_offset,
        )

    def is_clicked(self, click_pos: Vector2) -> bool:
        """
        Determine if the clicked location is on the BotRenderer icon.

        Parameters
        ----------
        click_pos
            The position of the click in window coordinates.

        Returns
        -------
        bool
            True if the click position is within or on the icon radius.
        """
        return point_in_or_on_circle(click_pos, self.pos_v, BotRenderer.ICON_RADIUS)


def _to_display_radians(bearing_deg: float) -> float:
    """Convert bearing (degrees) to Pygame-compatible angle (radians).

    For use in e.g. calls to `pygame.draw.arc`

    Parameters
    ----------
    bearing_deg
        Conventional bearing angle in degrees CCW from North

    Returns
    -------
    float
        Pygame-compatible angle in radians CW from East

    """
    return radians(-bearing_deg + 90)
