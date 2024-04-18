"""View class: renders a World using Pygame."""


from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.observer import Observer
from two_d_game_ai.render import colors
from two_d_game_ai.render.botrenderer import BotRenderer

if TYPE_CHECKING:
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

    Non-public attributes (incomplete)
    ----------------------------------
    _bot_renderers: list[BotRenderer]
        All Bot render instances
    """

    CAPTION = "2dGameAI"
    FONT_SIZE = 24

    def __init__(self, world: World, name: str, scale_factor: float = 1) -> None:
        super().__init__(name)
        self._bot_renderers = []
        self.world = world
        self.scale_factor = scale_factor

        self._max_render_fps = 1 / SIMULATION_STEP_INTERVAL_S

        self.running = True

        pygame.init()
        self._font = pygame.font.Font(None, self.FONT_SIZE)
        window_dimension = world.radius * 2 * self.scale_factor
        self.window = pygame.display.set_mode(
            (
                window_dimension,
                window_dimension,
            ),
        )
        self._display_offset = self.scale_factor * Vector2(
            self.world.radius, self.world.radius
        )
        pygame.display.set_caption(self.CAPTION)
        self._clock = pygame.Clock()

        for bot in world.bots:
            bot.register_observer(self)
            self._bot_renderers.append(
                BotRenderer(
                    view=self,
                    bot=bot,
                    font=self._font,
                )
            )

        self._selected: None | BotRenderer = None

    def handle_inputs(self) -> None:
        """Handle user inputs."""
        for event in pygame.event.get():

            # WINDOW/HIGH LEVEL EVENTS
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False

            # MOUSE EVENTS
            elif (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):  # normally left-click
                self._selected = self._get_clicked(event.pos)
                for bot_renderer in self._bot_renderers:
                    bot_renderer.highlight = False
                    if bot_renderer is self._selected:
                        bot_renderer.highlight = True

            # KEYBOARD EVENTS
            elif (
                event.type == pygame.KEYDOWN and event.key == pygame.K_p
            ):  # toggle [P]ause
                self.world.is_paused = not self.world.is_paused

    def render(self) -> None:
        """Render the World to the Pygame window.

        Drawn in order, bottom layer to top.
        """
        # Limit update rate to save CPU
        self._clock.tick(self._max_render_fps)

        self.window.fill(colors.BACKGROUND)
        self._draw_world_limits()

        for bot_renderer in self._bot_renderers:
            bot_renderer.draw()
        self._draw_step_counter()

        # update entire display
        pygame.display.flip()

    def _get_clicked(self, click_pos: Vector2) -> BotRenderer | None:
        for bot_renderer in self._bot_renderers:
            if bot_renderer.is_clicked(click_pos):
                log_msg = f"{bot_renderer.bot.name} clicked."
                logging.info(log_msg)
                return bot_renderer
        return None

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


        text_content = (
                f"sim elapsed: {elapsed_time:.1f} s\n"
                f"sim step: {self.world.step_counter}\n"
            )
        if self.world.is_paused:
            text_content += "paused"
        text = self._font.render(
            text=text_content,
            antialias=True,
            color=colors.LABEL,
        )
        self.window.blit(text, (0, 0))

    def to_display(self, world_pos: Vector2) -> Vector2:
        """Convert world coordinates to Pygame display window coordinates.

        Parameters
        ----------
        world_pos
            World coordinates

        Returns
        -------
        Vector2
            Display window coordinates.
            Origin is at centre, positive y upwards.
        """
        pos = world_pos.copy()
        pos.y = -pos.y
        pos *= self.scale_factor
        return pos + self._display_offset

    def from_display(self, display_pos: Vector2) -> Vector2:
        """Convert Pygame window coordinates to world coordinates.
        coordinates.

        Parameters
        ----------
        display_pos
            Display window coordinates.
            Origin is at centre, positive y upwards.

        Returns
        -------
        Vector2
            World coordinates.
        """
        pos = display_pos - self._display_offset
        pos /= self.scale_factor
        pos.y = -pos.y
        return pos
