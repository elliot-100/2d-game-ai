"""Module containing `View` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Rect, Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.entities import Bot
from two_d_game_ai.entities.observer_pattern import _Observer
from two_d_game_ai.render import colors
from two_d_game_ai.render.bot_renderer import BotRenderer
from two_d_game_ai.render.movement_block_renderer import MovementBlockRenderer
from two_d_game_ai.render.primitives import draw_scaled_line, draw_scaled_rect

if TYPE_CHECKING:
    from two_d_game_ai.world import World

_PRIMARY_MOUSE_BUTTON = 1
_SECONDARY_MOUSE_BUTTON = 3


class View(_Observer):
    """Renders window, World and decorations.

    NB: Unlike Pygame default, origin at centre, positive y upwards.
    """

    FONT_SIZE: ClassVar[int] = 24
    """Base font size for all text."""

    _CAPTION: ClassVar[str] = "2dGameAI"
    _MAX_RENDER_FPS: ClassVar[float] = 1 / SIMULATION_STEP_INTERVAL_S

    def __init__(
        self,
        world: World,
        name: str,
        scale_factor: float = 1,
        margin: int = 0,
    ) -> None:
        self.world = world
        """The `World` to be rendered."""
        super().__init__(name)
        self.scale_factor = scale_factor
        """Scale factor applied to the `World`."""
        self.margin = margin
        """Margin in display units applied to all sides of the `World`."""

        pygame.init()
        self._font = pygame.font.Font(None, self.FONT_SIZE)

        _window_size = self.world.size * self.scale_factor + 2 * self.margin
        self.window = pygame.display.set_mode((_window_size, _window_size))
        """Top level Pygame `Surface`."""

        pygame.display.set_caption(self._CAPTION)
        self._clock = pygame.Clock()
        self.running: bool = True
        """Flag to control e.g. input handling."""

        self._entity_renderers = [
            BotRenderer(view=self, entity=bot, font=self._font) for bot in world.bots
        ] + [
            MovementBlockRenderer(view=self, entity=block, font=self._font)
            for block in world.movement_blocks
        ]

        for bot in world.bots:
            bot.register_observer(self)
        self._selected: None | MovementBlockRenderer | BotRenderer = None

        self._DISPLAY_OFFSET = Vector2(
            self.world.size / 2,
            self.world.size / 2,
        ) * self.scale_factor + Vector2(
            self.margin,
            self.margin,
        )

    def handle_inputs(self) -> None:
        """Handle user inputs."""
        for event in pygame.event.get():
            match event.type:
                # WINDOW/HIGH LEVEL EVENTS
                case pygame.QUIT:  # user clicked window close
                    self.running = False

                # MOUSE EVENTS
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == _PRIMARY_MOUSE_BUTTON:
                        self._handle_mouse_select(event.pos)
                    elif event.button == _SECONDARY_MOUSE_BUTTON:
                        self._handle_mouse_set_destination(event.pos)

                # KEYBOARD EVENTS
                case pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # toggle [P]ause
                        self.world.is_paused = not self.world.is_paused

    def _handle_mouse_select(self, click_pos: Vector2) -> None:
        self._selected = self._clicked_entity(click_pos)
        for renderer in self._entity_renderers:
            renderer.is_selected = renderer == self._selected

    def _clicked_entity(
        self, click_pos: Vector2
    ) -> MovementBlockRenderer | BotRenderer | None:
        """Return the EntityRenderer at click position, or None."""
        for renderer in self._entity_renderers:
            if renderer.is_clicked(click_pos):
                log_msg = f"{renderer.entity.name} clicked."
                logging.info(log_msg)
                return renderer
        return None

    def _handle_mouse_set_destination(self, click_pos: Vector2) -> None:
        """Attempt to set destination, if applicable to current selection."""
        if isinstance(self._selected, BotRenderer) and isinstance(
            self._selected.entity, Bot
        ):
            self._selected.entity.destination_v = self.from_display(click_pos)

    def render(self) -> None:
        """Render the World to the Pygame window."""
        # Limit update rate to save CPU:
        self._clock.tick(self._MAX_RENDER_FPS)

        # Drawn in order, bottom layer to top:
        self.window.fill(colors.WINDOW_FILL)
        self._draw_world_limits()
        self._draw_grid()
        for renderer in self._entity_renderers:
            if isinstance(renderer, MovementBlockRenderer):
                renderer.draw()
        for renderer in self._entity_renderers:
            if isinstance(renderer, BotRenderer):
                renderer.draw()
        self._draw_step_counter()
        # update entire display
        pygame.display.flip()

    def _draw_world_limits(self) -> None:
        """Draw the World limits."""
        world_min = -self.world.size / 2
        world_max = self.world.size / 2
        world_size = self.world.size

        # Border
        draw_scaled_rect(
            self,
            colors.WORLD_FILL,
            Rect(
                (world_min, world_min),
                (world_size, world_size),
            ),
            width=0,
        )
        # Axes
        draw_scaled_line(
            self,
            colors.WORLD_AXES_LINE,
            Vector2(0, world_min),
            Vector2(0, world_max),
            width=3,
        )
        draw_scaled_line(
            self,
            colors.WORLD_AXES_LINE,
            Vector2(world_min, 0),
            Vector2(world_max, 0),
            width=3,
        )

    def _draw_grid(self) -> None:
        """Draw the Grid."""
        world_min = -self.world.size / 2
        world_max = self.world.size / 2
        grid_size = self.world.grid.size
        cell_size = self.world.size / grid_size

        for cell_index in range(-grid_size // 2, grid_size // 2 + 1):
            # horizontal grid line
            draw_scaled_line(
                self,
                colors.WORLD_GRID_LINE,
                Vector2(world_min, cell_index * cell_size),
                Vector2(world_max, cell_index * cell_size),
                width=1,
            )
            # vertical grid line
            draw_scaled_line(
                self,
                colors.WORLD_GRID_LINE,
                Vector2(cell_index * cell_size, world_min),
                Vector2(cell_index * cell_size, world_max),
                width=1,
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
            color=colors.WINDOW_TEXT,
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
        return pos + self._DISPLAY_OFFSET

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
        pos = display_pos - self._DISPLAY_OFFSET
        pos /= self.scale_factor
        pos.y = -pos.y
        return pos
