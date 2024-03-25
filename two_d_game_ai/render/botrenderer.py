"""BotRenderer class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Color, Font, Surface, Vector2

from two_d_game_ai.render import colors, to_display

if TYPE_CHECKING:
    from two_d_game_ai.bot import Bot


class BotRenderer:
    """Renders a Bot to a Surface.

    Provides methods to draw Bot icon and related elements.

    Attributes
    ----------
    bot: Bot
        The Bot to render
    surface: Surface
        Pygame Surface to render to
    scale_factor: float
        Rendering scale factor
    font: Font
        # TODO
    """

    ICON_RADIUS = 10  # in pixels
    LABEL_OFFSET = (10, 10)  # in pixels

    def __init__(
        self,
        *,
        bot: Bot,
        surface: Surface,
        scale_factor: float,
        font: Font,
    ) -> None:
        self.bot = bot
        self.surface = surface
        self.scale_factor = scale_factor
        self.font = font

    def draw_icon(self) -> None:
        """Draw unscaled icon to surface."""
        pygame.draw.circle(
            surface=self.surface,
            color=colors.FOREGROUND,
            center=to_display(self.bot.world, self.bot.pos, self.scale_factor),
            radius=self.ICON_RADIUS,
        )

        # Heading indicator (line from centre to 'nose')
        nose_offset = Vector2(0, self.ICON_RADIUS).rotate(-self.bot.heading_degrees)
        self._draw_scaled_line(
            color=colors.BACKGROUND,
            start_pos=self.bot.pos,
            end_pos=self.bot.pos + nose_offset,
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
            dest=self.bot.pos,
            display_offset=self.LABEL_OFFSET,
        )

    def draw_destination(self) -> None:
        """Draw Bot destination icon, and line to it."""
        if not self.bot.destination:
            raise TypeError

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.scale_factor
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.destination + Vector2(-offset, -offset),
            end_pos=self.bot.destination + Vector2(offset, offset),
        )
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.destination + Vector2(offset, -offset),
            end_pos=self.bot.destination + Vector2(-offset, offset),
        )

        # Line from Bot centre to destination
        self._draw_scaled_line(
            color=colors.FOREGROUND,
            start_pos=self.bot.pos,
            end_pos=self.bot.destination,
        )

    def draw_visible_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other visible Bot."""
        self._draw_scaled_line(
            color=colors.VISION,
            start_pos=self.bot.pos,
            end_pos=other_bot.pos,
            width=4,
        )

    def draw_known_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other known Bot."""
        self._draw_scaled_line(
            color=colors.KNOWS,
            start_pos=self.bot.pos,
            end_pos=other_bot.pos,
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
            surface=self.surface,
            color=color,
            start_pos=to_display(self.bot.world, start_pos, self.scale_factor),
            end_pos=to_display(self.bot.world, end_pos, self.scale_factor),
            width=width,
        )

    def _scaled_blit(
        self,
        *,
        source: Surface,
        dest: Vector2,
        display_offset: tuple[int, int],
    ) -> None:
        self.surface.blit(
            source=source,
            dest=to_display(self.bot.world, dest, self.scale_factor) + display_offset,
        )
