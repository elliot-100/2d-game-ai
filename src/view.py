"""Renderer using Pygame."""

import pygame
from pygame import Vector2

from src.bot import Bot
from src.world import World


class View:
    """The View class.

    NB: Unlike Pygame default, origin at centre, positive y upwards

    Attributes
    ----------
    world
        World to be viewed
    window
        Top level 'display surface'
    """

    BACKGROUND_COLOR = GREY_80 = (51, 51, 51)
    FOREGROUND_COLOR = RED = (255, 0, 0)
    LABEL_COLOR = WHITE = (255, 255, 255)
    DISPLAY_MAX_FPS = 60
    CAPTION = "2dGameAI"
    FONT_SIZE = 24
    ICON_RADIUS = 10
    LABEL_OFFSET = Vector2(10, 10)

    def __init__(self, world: World) -> None:
        """Wrap Pygame window initialisation."""
        self.world = world
        self.running = True

        pygame.init()
        self.font = pygame.font.Font(None, View.FONT_SIZE)
        self.window = pygame.display.set_mode((world.radius * 2, world.radius * 2))
        pygame.display.set_caption(View.CAPTION)
        self.clock = pygame.Clock()

    def render(self) -> None:
        """Output a representation of the world to the window."""
        # Limit update rate to save CPU
        self.clock.tick(View.DISPLAY_MAX_FPS)
        # render background
        self.window.fill(View.BACKGROUND_COLOR)
        # render world limits
        pygame.draw.circle(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(Vector2(0, 0)),
            self.world.radius,
            1,
        )
        # render all bots as icons
        for bot in self.world.bots.values():
            self.draw_bot(bot)

        # render the step counter...
        text = self.font.render(
            text=(
                f"sim elapsed: {self.world.step_counter/60:.1f} s\n"
                f"sim step: {self.world.step_counter}"
            ),
            antialias=True,
            color=View.FOREGROUND_COLOR,
        )
        # ...and blit to window
        self.window.blit(text, (0, 0))

        # update entire display
        pygame.display.flip()

    def to_display(self, world_pos: Vector2) -> Vector2:
        """Convert world coordinates to window coordinates.

        Parameters
        ----------
        world_pos
            World coordinates

        Returns
        -------
        Window coordinates, with origin at centre
        """
        display_pos = (world_pos[0], -world_pos[1])
        offset = Vector2(self.world.radius, self.world.radius)
        return display_pos + offset

    def handle_window_close(self) -> None:
        """Wrap Pygame window close handling."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False

    def draw_bot(self, bot: Bot) -> None:
        """Draw unscaled Bot icon."""
        # Filled circle
        pygame.draw.circle(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(bot.pos),
            View.ICON_RADIUS,
            0,
        )

        # Heading indicator
        # TODO: refactor
        nose_offset = Vector2(View.ICON_RADIUS, 0).rotate(bot.heading.as_polar()[1])
        pygame.draw.line(
            self.window,
            View.BACKGROUND_COLOR,
            self.to_display(bot.pos),
            self.to_display(bot.pos + nose_offset),
            3,
        )

        # Create name label
        label = self.font.render(
            text=bot.name,
            antialias=True,
            color=View.LABEL_COLOR,
        )
        # ...and blit to window
        self.window.blit(label, self.to_display(bot.pos) + View.LABEL_OFFSET)
