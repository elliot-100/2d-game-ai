"""Renderer using Pygame."""

import pygame
from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bot import Bot
from two_d_game_ai.observer import Observer
from two_d_game_ai.world import World


class View(Observer):
    """The View class.

    NB: Unlike Pygame default, origin at centre, positive y upwards

    Attributes
    ----------
    world
        The World to be viewed
    window
        Top level 'display surface'
    """

    BACKGROUND_COLOR = GREY_80 = (51, 51, 51)
    FOREGROUND_COLOR = RED = (255, 0, 0)
    LABEL_COLOR = WHITE = (255, 255, 255)
    VISION_COLOR = BLUE = (102, 102, 255)
    CAPTION = "2dGameAI"
    FONT_SIZE = 24
    ICON_RADIUS = 10
    LABEL_OFFSET = Vector2(10, 10)

    def __init__(self, world: World, name: str) -> None:
        super().__init__(name)
        self.world = world

        self.max_render_fps = 1 / SIMULATION_STEP_INTERVAL_S

        self.running = True

        pygame.init()
        self.font = pygame.font.Font(None, View.FONT_SIZE)
        self.window = pygame.display.set_mode((world.radius * 2, world.radius * 2))
        pygame.display.set_caption(View.CAPTION)
        self.clock = pygame.Clock()

        for bot in world.bots.values():
            bot.register_observer(self)

    def render(self) -> None:
        """Output a representation of the world to the window."""
        # Limit update rate to save CPU
        self.clock.tick(self.max_render_fps)
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
                "sim elapsed: "
                f"{self.world.step_counter * SIMULATION_STEP_INTERVAL_S:.1f} s\n"
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
        Vector2
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
        """Draw unscaled Bot icon and decorations.

        Drawn in order, bottom layer to top.
        """
        if bot.destination:
            self.draw_bot_destination_icon(bot)
        if bot.visible_bots:
            for visible_bot in bot.visible_bots:
                self.draw_bot_visible_line(bot, visible_bot)
        self.draw_bot_icon(bot)
        self.draw_bot_label(bot)

    def draw_bot_destination_icon(self, bot: Bot) -> None:
        """Draw Bot destination icon and line to it."""
        # Destination marker (X)
        if not bot.destination:
            raise TypeError
        offset = self.ICON_RADIUS
        pygame.draw.line(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(bot.destination + Vector2(-offset, -offset)),
            self.to_display(bot.destination + Vector2(offset, offset)),
            1,
        )
        pygame.draw.line(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(bot.destination + Vector2(offset, -offset)),
            self.to_display(bot.destination + Vector2(-offset, offset)),
            1,
        )

        # Line from Bot centre to destination
        pygame.draw.line(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(bot.pos),
            self.to_display(bot.destination),
            1,
        )

    def draw_bot_icon(self, bot: Bot) -> None:
        """Draw Bot icon."""
        # Filled circle
        pygame.draw.circle(
            self.window,
            View.FOREGROUND_COLOR,
            self.to_display(bot.pos),
            View.ICON_RADIUS,
            0,
        )

        # Heading indicator (line from centre to edge of icon)
        nose_offset = Vector2(View.ICON_RADIUS, 0).rotate(bot.heading.as_polar()[1])
        pygame.draw.line(
            self.window,
            View.BACKGROUND_COLOR,
            self.to_display(bot.pos),
            self.to_display(bot.pos + nose_offset),
            3,
        )

    def draw_bot_label(self, bot: Bot) -> None:
        """Draw Bot name label."""
        label = self.font.render(
            text=bot.name,
            antialias=True,
            color=View.LABEL_COLOR,
        )
        self.window.blit(label, self.to_display(bot.pos) + View.LABEL_OFFSET)

    def draw_bot_visible_line(self, bot: Bot, other_bot: Bot) -> None:
        """Draw line from Bot to other visible Bot."""
        pygame.draw.line(
            self.window,
            View.VISION_COLOR,
            self.to_display(bot.pos),
            self.to_display(other_bot.pos),
            2,
        )
