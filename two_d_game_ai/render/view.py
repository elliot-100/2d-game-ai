"""Renderer using Pygame."""

import pygame
from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bot import Bot
from two_d_game_ai.observer import Observer
from two_d_game_ai.render import (
    BACKGROUND_COLOR,
    CAPTION,
    FONT_SIZE,
    FOREGROUND_COLOR,
    to_display,
)
from two_d_game_ai.render.botrenderer import BotRenderer
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

    def __init__(self, world: World, name: str) -> None:
        super().__init__(name)
        self.world = world

        self.max_render_fps = 1 / SIMULATION_STEP_INTERVAL_S

        self.running = True

        pygame.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.window = pygame.display.set_mode((world.radius * 2, world.radius * 2))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.Clock()

        for bot in world.bots:
            bot.register_observer(self)

    def render(self) -> None:
        """Output a representation of the world to the window.

        Drawn in order, bottom layer to top.
        """
        # Limit update rate to save CPU
        self.clock.tick(self.max_render_fps)
        # render background
        self.window.fill(BACKGROUND_COLOR)
        # render world limits
        pygame.draw.circle(
            self.window,
            FOREGROUND_COLOR,
            to_display(self.world, Vector2(0, 0)),
            self.world.radius,
            1,
        )
        # render all bots as icons
        for bot in self.world.bots:
            self.draw_bot(bot)

        # render the step counter...
        text = self.font.render(
            text=(
                "sim elapsed: "
                f"{self.world.step_counter * SIMULATION_STEP_INTERVAL_S:.1f} s\n"
                f"sim step: {self.world.step_counter}"
            ),
            antialias=True,
            color=FOREGROUND_COLOR,
        )
        # ...and blit to window
        self.window.blit(text, (0, 0))

        # update entire display
        pygame.display.flip()

    def handle_window_close(self) -> None:
        """Wrap Pygame window close handling."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False

    def draw_bot(self, bot: Bot) -> None:
        """Draw unscaled Bot icon and decorations.

        Drawn in order, bottom layer to top.
        """
        bot_renderer = BotRenderer(
            bot=bot,
            surface=self.window,
            font=self.font,
        )
        if bot.destination:
            bot_renderer.draw_destination()
        if bot.visible_bots:
            for visible_bot in bot.visible_bots:
                bot_renderer.draw_visible_line(bot, visible_bot)
        if bot.known_bots:
            for known_bot in bot.known_bots:
                bot_renderer.draw_known_line(bot, known_bot)
        bot_renderer.draw_icon()
        bot_renderer.draw_label()
