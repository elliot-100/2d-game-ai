"""View class: renders a World using Pygame."""

import logging

import pygame
from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.observer import Observer
from two_d_game_ai.render import colors
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

    def handle_inputs(self) -> None:
        """Wrap Pygame window close handling."""
        # TODO: More efficient event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = Vector2(event.pos)
                log_msg = (
                    f"Mouse button {event.button} pressed at window {click_pos}"
                )
                logging.info(log_msg)

    def render(self) -> None:
        """Render the World to the Pygame window.

        Drawn in order, bottom layer to top.
        """
        # Limit update rate to save CPU
        self.clock.tick(self.max_render_fps)

        self.window.fill(colors.BACKGROUND)
        self._draw_world_limits()
        for bot in self.world.bots:
            BotRenderer(
                view=self,
                bot=bot,
                font=self.font,
            ).draw()
        self._draw_step_counter()

        # update entire display
        pygame.display.flip()

    def _draw_world_limits(self) -> None:
        """Draw the World limits as a circle."""
        pygame.draw.circle(
            self.window,
            colors.FOREGROUND,
            self.to_display(Vector2(0, 0)),
            self.world.radius * self.scale_factor,
            1,
        )

    def _draw_step_counter(self) -> None:
        """Render the step counter and blit to window."""
        elapsed_time = self.world.step_counter * SIMULATION_STEP_INTERVAL_S
        text = self.font.render(
            text=(
                f"sim elapsed: {elapsed_time:.1f} s\n"
                f"sim step: {self.world.step_counter}"
            ),
            antialias=True,
            color=colors.LABEL,
        )
        self.window.blit(text, (0, 0))

    def to_display(self, world_pos: Vector2) -> Vector2:
        """Convert world coordinates to Pygame-compatible coordinates.

        Parameters
        ----------
        world_pos
            World coordinates

        Returns
        -------
        Vector2
            Display window coordinates.
            Origin is at centre, positive y upwards (opposite to Pygame, etc).
        """
        display_pos = self.scale_factor * Vector2(world_pos.x, -world_pos.y)
        offset = self.scale_factor * Vector2(self.world.radius, self.world.radius)
        return display_pos + offset
