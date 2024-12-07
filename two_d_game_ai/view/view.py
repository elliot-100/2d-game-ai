"""Module containing `View` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Rect, Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.observer_pattern import Observer
from two_d_game_ai.view import colors
from two_d_game_ai.view.bot_renderer import BotRenderer
from two_d_game_ai.view.movement_block_renderer import MovementBlockRenderer
from two_d_game_ai.view.primitives import draw_scaled_line, draw_scaled_rect
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from two_d_game_ai.world.grid_ref import GridRef
    from two_d_game_ai.world.world import World

_PRIMARY_MOUSE_BUTTON = 1
_SECONDARY_MOUSE_BUTTON = 3


class View(Observer):
    """Renders a `two_d_game_ai.world.world.World` to a window.

    NB: Unlike Pygame default, origin at centre, positive y upwards.
    """

    FONT_SIZE: ClassVar[int] = 24
    """Base font size for all text."""

    _CAPTION: ClassVar[str] = "2dGameAI"
    _MAX_RENDER_FPS: ClassVar = SIMULATION_FPS

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
        self._margin = margin
        """Margin in display units applied to all sides of the `World`."""

        pygame.init()
        self._font = pygame.font.Font(None, self.FONT_SIZE)

        _window_size = self.world.size * self.scale_factor + 2 * self._margin
        self.window = pygame.display.set_mode((_window_size, _window_size))
        """Top level Pygame `Surface`."""

        pygame.display.set_caption(self._CAPTION)
        self._clock = pygame.Clock()
        self.running: bool = True
        """Flag to control e.g. input handling."""

        self._initialize_renderers()

        self._world_max = self.world.size / 2
        self._world_min = -self._world_max

        self._display_offset = Vector2(
            self._world_max,
            self._world_max,
        ) * self.scale_factor + Vector2(
            self._margin,
            self._margin,
        )

    def _initialize_renderers(self) -> None:
        self._renderers = [
            BotRenderer(view=self, entity=bot, font=self._font)
            for bot in self.world.bots
        ] + [
            MovementBlockRenderer(view=self, entity=block, font=self._font)
            for block in self.world.movement_blocks
        ]
        for bot in self.world.bots:
            bot.register_observer(self)
        self._selected: None | MovementBlockRenderer | BotRenderer = None

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
        for renderer in self._renderers:
            renderer.is_selected = renderer == self._selected

    def _clicked_entity(
        self, click_pos: Vector2
    ) -> MovementBlockRenderer | BotRenderer | None:
        """Return the EntityRenderer at click position, or None."""
        for renderer in self._renderers:
            if renderer.is_clicked(click_pos):
                log_msg = f"{renderer.entity.name} clicked."
                logging.info(log_msg)
                return renderer
        return None

    def _handle_mouse_set_destination(self, click_pos: Vector2) -> None:
        """Attempt to set destination, if applicable to current selection."""
        clicked_grid_ref = self._clicked_grid_ref(click_pos)
        if (
            isinstance(self._selected, BotRenderer)
            and isinstance(self._selected.entity, Bot)
            and self.world.grid.is_traversable(clicked_grid_ref)
        ):
            self._selected.entity.destination = self._to_world(click_pos)

    def _clicked_grid_ref(self, click_pos: Vector2) -> GridRef:
        """Return the GridRef at click position, or None."""
        return Grid.cell_from_world_pos(self.world, self._to_world(click_pos))

    def render(self) -> None:
        """Render the `World` to the Pygame window."""
        # Limit update rate to save CPU:
        self._clock.tick(self._MAX_RENDER_FPS)

        # Drawn in order, bottom layer to top:
        self.window.fill(colors.WINDOW_FILL)
        self._draw_world_limits()
        self._draw_grid()
        for renderer in self._renderers:
            renderer.draw()
        self._draw_step_counter()
        # update entire display
        pygame.display.flip()

    def _draw_world_limits(self) -> None:
        """Draw the `World` limits."""
        # Border
        draw_scaled_rect(
            self,
            colors.WORLD_FILL,
            Rect(
                (self._world_min, self._world_min),
                (self.world.size, self.world.size),
            ),
            width=0,
        )
        # Axes
        draw_scaled_line(  # Y
            self,
            colors.WORLD_AXES_LINE,
            Vector2(0, self._world_min),
            Vector2(0, self._world_max),
            width=3,
        )
        draw_scaled_line(  # X
            self,
            colors.WORLD_AXES_LINE,
            Vector2(self._world_min, 0),
            Vector2(self._world_max, 0),
            width=3,
        )

    def _draw_grid(self) -> None:
        """Draw the `Grid`."""
        grid_size = self.world.grid.size
        cell_size = self.world.size / grid_size

        for cell_index in range(-grid_size // 2, grid_size // 2 + 1):
            # horizontal grid line
            draw_scaled_line(
                self,
                colors.WORLD_GRID_LINE,
                Vector2(self._world_min, cell_index * cell_size),
                Vector2(self._world_max, cell_index * cell_size),
                width=1,
            )
            # vertical grid line
            draw_scaled_line(
                self,
                colors.WORLD_GRID_LINE,
                Vector2(cell_index * cell_size, self._world_min),
                Vector2(cell_index * cell_size, self._world_max),
                width=1,
            )

        for cell_ref in self.world.grid.untraversable_cells:
            draw_scaled_rect(
                self,
                colors.MOVEMENT_BLOCK_FILL,
                Rect(
                    (cell_ref.x * cell_size, cell_ref.y * cell_size),
                    (cell_size, cell_size),
                ),
                width=0,
            )

    def _draw_step_counter(self) -> None:
        """Render the step counter and blit to window."""
        elapsed_time = self.world.step_counter / SIMULATION_FPS

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
        """Convert `World` coordinates to window coordinates.

        Parameters
        ----------
        world_pos
            `World` coordinates

        Returns
        -------
        Vector2
            Display window coordinates.
            Origin is at centre, positive y upwards.
        """
        return (
            world_pos.reflect(Vector2(0, 1)) * self.scale_factor + self._display_offset
        )

    def _to_world(self, display_pos: Vector2) -> Vector2:
        """Convert window coordinates to `World` coordinates.

        Parameters
        ----------
        display_pos
            Display window coordinates.
            Origin is at centre, positive y upwards.

        Returns
        -------
        Vector2
            `World` coordinates.
        """
        pos = (display_pos - self._display_offset) / self.scale_factor
        pos.y = -pos.y
        return pos
