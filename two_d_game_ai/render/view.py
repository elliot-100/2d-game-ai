"""View class: Renderer using Pygame."""

import pygame
from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bot import Bot
from two_d_game_ai.observer import Observer
from two_d_game_ai.render import colors, to_display
from two_d_game_ai.render.botrenderer import BotRenderer
from two_d_game_ai.world import World


class View(Observer):
    """Renders window, World and decorations.

    NB: Unlike Pygame default, origin at centre, positive y upwards

    Attributes
    ----------
    name: str
    world: World
        The World to be viewed
    scale_factor: float
        Rendering scale factor
    window: Window
        Top level Pygame Surface.
    """

    CAPTION = "2dGameAI"
    FONT_SIZE = 24

    def __init__(self, world: World, name: str, scale_factor: float = 1) -> None:
        super().__init__(name)
        self.world = world
        self.scale_factor = scale_factor

        self.max_render_fps = 1 / SIMULATION_STEP_INTERVAL_S

        self.running = True

        pygame.init()
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        window_dimension = world.radius * 2 * self.scale_factor
        self.window = pygame.display.set_mode(
            (
                window_dimension,
                window_dimension,
            ),
        )
        pygame.display.set_caption(self.CAPTION)
        self.clock = pygame.Clock()

        for bot in world.bots:
            bot.register_observer(self)

    def handle_window_close(self) -> None:
        """Wrap Pygame window close handling."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False

    def render(self) -> None:
        """Render the World to the Pygame window.

        Drawn in order, bottom layer to top.
        """
        # Limit update rate to save CPU
        self.clock.tick(self.max_render_fps)

        self.window.fill(colors.BACKGROUND)
        self.draw_world_limits()
        for bot in self.world.bots:
            self.draw_bot(bot)
        self.draw_step_counter()

        # update entire display
        pygame.display.flip()

    def draw_world_limits(self) -> None:
        """Draw the World limits as a circle."""
        pygame.draw.circle(
            self.window,
            colors.FOREGROUND,
            to_display(self.world, Vector2(0, 0), self.scale_factor),
            self.world.radius * self.scale_factor,
            1,
        )

    def draw_bot(self, bot: Bot) -> None:
        """Draw a Bot and decorations.

        Drawn in order, bottom layer to top.

        Attributes
        ----------
        bot: Bot
            The Bot to render
        """
        bot_renderer = BotRenderer(
            bot=bot,
            surface=self.window,
            scale_factor=self.scale_factor,
            font=self.font,
        )
        if bot.destination:
            bot_renderer.draw_destination()
        if bot.visible_bots:
            for visible_bot in bot.visible_bots:
                bot_renderer.draw_visible_line(visible_bot)
        if bot.known_bots:
            for known_bot in bot.known_bots:
                bot_renderer.draw_known_line(known_bot)
        bot_renderer.draw_icon()
        bot_renderer.draw_label()

    def draw_step_counter(self) -> None:
        """Render the step counter and blit to window."""
        text = self.font.render(
            text=(
                "sim elapsed: "
                f"{self.world.step_counter * SIMULATION_STEP_INTERVAL_S:.1f} s\n"
                f"sim step: {self.world.step_counter}"
            ),
            antialias=True,
            color=colors.LABEL,
        )
        self.window.blit(text, (0, 0))
