"""TO DO."""
import pygame
from pygame import Font, Surface, Vector2

from two_d_game_ai.bot import Bot
from two_d_game_ai.render import BACKGROUND_COLOR, FOREGROUND_COLOR, to_display


class BotRenderer:
    """Renderer for a Bot.

    Provides methods to draw Bot icon and related elements.

    Attributes
    ----------
    bot: Bot
    surface: Surface
    font: Font
    """

    ICON_RADIUS = 10
    LABEL_OFFSET = (10, 10)
    LABEL_COLOR = WHITE = (255, 255, 255)
    VISION_COLOR = BLUE_LIGHT = (153, 153, 255)
    KNOWN_COLOR = BLUE_DARK = (102, 102, 255)

    def __init__(
        self,
        *,
        bot: Bot,
        surface: Surface,
        font: Font,
    ) -> None:
        self.bot = bot
        self.surface = surface
        self.font = font

    def draw_icon(self) -> None:
        """TO DO."""
        pygame.draw.circle(
            self.surface,
            FOREGROUND_COLOR,
            to_display(self.bot.world, self.bot.pos),
            self.ICON_RADIUS,
            0,
        )

        # Heading indicator (line from centre to edge of icon)
        # TODO: review the '-' here - tactical fix
        nose_offset = Vector2(self.ICON_RADIUS, 0).rotate(
            -self.bot.heading.as_polar()[1],
        )
        pygame.draw.line(
            self.surface,
            BACKGROUND_COLOR,
            to_display(self.bot.world, self.bot.pos),
            to_display(self.bot.world, self.bot.pos) + nose_offset,
            3,
        )

    def draw_label(self) -> None:
        """Draw Bot name label."""
        label = self.font.render(
            text=self.bot.name,
            antialias=True,
            color=self.LABEL_COLOR,
        )
        self.surface.blit(
            label,
            to_display(self.bot.world, self.bot.pos) + self.LABEL_OFFSET,
        )

    def draw_destination(self) -> None:
        """Draw Bot destination icon and line to it."""
        if not self.bot.destination:
            raise TypeError

        # Destination marker (X)
        offset = self.ICON_RADIUS
        pygame.draw.line(
            self.surface,
            FOREGROUND_COLOR,
            to_display(
                self.bot.world,
                self.bot.destination + Vector2(-offset, -offset),
            ),
            to_display(self.bot.world, self.bot.destination + Vector2(offset, offset)),
            1,
        )
        pygame.draw.line(
            self.surface,
            FOREGROUND_COLOR,
            to_display(self.bot.world, self.bot.destination + Vector2(offset, -offset)),
            to_display(self.bot.world, self.bot.destination + Vector2(-offset, offset)),
            1,
        )

        # Line from Bot centre to destination
        pygame.draw.line(
            self.surface,
            FOREGROUND_COLOR,
            to_display(self.bot.world, self.bot.pos),
            to_display(self.bot.world, self.bot.destination),
            1,
        )

    def draw_visible_line(self, bot: Bot, other_bot: Bot) -> None:
        """Draw line from Bot to other visible Bot."""
        pygame.draw.line(
            self.surface,
            self.VISION_COLOR,
            to_display(self.bot.world, bot.pos),
            to_display(self.bot.world, other_bot.pos),
            4,
        )

    def draw_known_line(self, bot: Bot, other_bot: Bot) -> None:
        """Draw line from Bot to other known Bot."""
        pygame.draw.line(
            self.surface,
            self.KNOWN_COLOR,
            to_display(self.bot.world, bot.pos),
            to_display(self.bot.world, other_bot.pos),
            1,
        )
