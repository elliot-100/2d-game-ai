"""BotRenderer class."""
import pygame
from pygame import Font, Surface, Vector2

from two_d_game_ai.bot import Bot
from two_d_game_ai.render import BACKGROUND_COLOR, FOREGROUND_COLOR, to_display

AppColor = tuple[int, int, int]


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
            self.surface,
            FOREGROUND_COLOR,
            to_display(self.bot.world, self.bot.pos, self.scale_factor),
            self.ICON_RADIUS,
            0,
        )

        # Heading indicator (line from centre to 'nose')
        nose_offset = Vector2(self.ICON_RADIUS, 0).rotate(
            self.bot.heading.as_polar()[1],
        )
        self._draw_scaled_line(
            BACKGROUND_COLOR,
            self.bot.pos,
            self.bot.pos + nose_offset,
            3,
        )

    def draw_label(self) -> None:
        """Draw Bot name label to surface."""
        label = self.font.render(
            text=self.bot.name,
            antialias=True,
            color=self.LABEL_COLOR,
        )
        self.surface.blit(
            label,
            to_display(self.bot.world, self.bot.pos, self.scale_factor)
            + self.LABEL_OFFSET,
        )

    def draw_destination(self) -> None:
        """Draw Bot destination icon, and line to it."""
        if not self.bot.destination:
            raise TypeError

        # Destination marker (X)
        offset = self.ICON_RADIUS / self.scale_factor
        self._draw_scaled_line(
            FOREGROUND_COLOR,
            self.bot.destination + Vector2(-offset, -offset),
            self.bot.destination + Vector2(offset, offset),
            1,
        )
        self._draw_scaled_line(
            FOREGROUND_COLOR,
            self.bot.destination + Vector2(offset, -offset),
            self.bot.destination + Vector2(-offset, offset),
            1,
        )

        # Line from Bot centre to destination
        self._draw_scaled_line(
            FOREGROUND_COLOR,
            self.bot.pos,
            self.bot.destination,
            1,
        )

    def draw_visible_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other visible Bot."""
        self._draw_scaled_line(
            self.VISION_COLOR,
            self.bot.pos,
            other_bot.pos,
            4,
        )

    def draw_known_line(self, other_bot: Bot) -> None:
        """Draw line from Bot to other known Bot."""
        self._draw_scaled_line(
            self.KNOWN_COLOR,
            self.bot.pos,
            other_bot.pos,
            1,
        )

    def _draw_scaled_line(
        self,
        color: AppColor,
        start_pos: Vector2,
        end_pos: Vector2,
        width: int,
    ) -> None:
        pygame.draw.line(
            self.surface,
            color,
            to_display(self.bot.world, start_pos, self.scale_factor),
            to_display(self.bot.world, end_pos, self.scale_factor),
            width,
        )
