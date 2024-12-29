"""Module containing `View` class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Color, Rect, Surface, Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.observer_pattern import Observer
from two_d_game_ai.view import colors
from two_d_game_ai.view.bot_renderer import BotRenderer
from two_d_game_ai.view.movement_block_renderer import MovementBlockRenderer
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
        self._bot_renderers = {
            BotRenderer(view=self, entity=bot, font=self._font)
            for bot in self.world.bots
        }
        self._block_renderers = {
            MovementBlockRenderer(view=self, entity=block, font=self._font)
            for block in self.world.movement_blocks
        }
        self._clickables = self._bot_renderers | self._block_renderers

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
        for renderer in self._clickables:
            renderer.is_selected = renderer == self._selected

    def _clicked_entity(
        self, click_pos: Vector2
    ) -> MovementBlockRenderer | BotRenderer | None:
        """Return the EntityRenderer at click position, or None."""
        for renderer in self._clickables:
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
        for _ in self._bot_renderers:
            _.draw()
        for _ in self._block_renderers:
            _.draw()
        self._draw_axes()

        self._draw_step_counter()
        # update entire display
        pygame.display.flip()

    def _draw_world_limits(self) -> None:
        """Draw the `World` limits."""
        # Border
        self.draw_rect(
            color=colors.WORLD_FILL,
            rect=Rect(
                (self._world_min, self._world_min),
                (self.world.size, self.world.size),
            ),
        )

    def _draw_axes(self) -> None:
        self.draw_line(  # Y
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(0, self._world_min),
            end_pos=Vector2(0, self._world_max),
        )
        self.draw_line(  # X
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(self._world_min, 0),
            end_pos=Vector2(self._world_max, 0),
        )

    def _draw_grid(self) -> None:
        """Draw the `Grid`."""
        grid_size = self.world.grid.size
        cell_size = self.world.size / grid_size

        for cell_index in range(grid_size + 1):
            cell_offset = cell_size * (cell_index - grid_size / 2)
            # horizontal grid line
            self.draw_line(
                color=colors.WORLD_GRID_LINE,
                start_pos=Vector2(self._world_min, cell_offset),
                end_pos=Vector2(self._world_max, cell_offset),
                width=1,
                anti_alias=False,
            )
            # vertical grid line
            self.draw_line(
                color=colors.WORLD_GRID_LINE,
                start_pos=Vector2(cell_offset, self._world_min),
                end_pos=Vector2(cell_offset, self._world_max),
                width=1,
                anti_alias=False,
            )

        oversize_px = 2
        for cell_ref in self.world.grid.untraversable_cells:
            grid_rect = Rect(
                (cell_ref.x * cell_size, cell_ref.y * cell_size), (cell_size, cell_size)
            )
            # draw slightly oversize to hide gridlines
            oversize_grid_rect = grid_rect.move(
                -int(oversize_px / self.scale_factor),
                -int(oversize_px / self.scale_factor),
            )
            oversize_grid_rect.width = oversize_grid_rect.height = int(
                grid_rect.width + 2 * oversize_px / self.scale_factor
            )
            self.draw_rect(
                color=colors.MOVEMENT_BLOCK_FILL,
                rect=Rect(oversize_grid_rect),
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

    def draw_line(
        self,
        *,
        color: Color,
        start_pos: Vector2,
        end_pos: Vector2,
        width: int = 1,
        anti_alias: bool = True,
    ) -> None:
        """Draw a line in `World` units.

        `width`: display pixels.
        """
        if anti_alias and width == 1:
            pygame.draw.aaline(
                surface=self.window,
                color=color,
                start_pos=self.to_display(start_pos),
                end_pos=self.to_display(end_pos),
            )

        else:
            # pygame.draw.aaline() only draws single-pixel width lines
            pygame.draw.line(
                surface=self.window,
                color=color,
                start_pos=self.to_display(start_pos),
                end_pos=self.to_display(end_pos),
                width=width,
            )

    def draw_rect(
        self,
        *,
        color: Color,
        rect: Rect,
        width: int = 0,
    ) -> None:
        """Draw a rectangle in `World` units.

        `width`: display pixels.

        """
        scaled_pos = self.to_display(Vector2(rect.left, rect.top))
        scaled_width = rect.width * self.scale_factor
        scaled_height = rect.height * self.scale_factor
        pygame.draw.rect(
            surface=self.window,
            color=color,
            rect=(
                scaled_pos.x,
                scaled_pos.y - scaled_height,
                scaled_width,
                scaled_height,
            ),
            width=width,
        )

    def draw_circle(
        self,
        *,
        color: Color,
        center: Vector2,
        radius: float,
        width: int = 0,
        scale_radius: bool = True,
    ) -> None:
        """Draw a circle in `World` units.

        Optionally supress radius scaling e.g. for icons whose size is independent
        of view scaling.

        `width`: display pixels.
        """
        if scale_radius:
            radius *= self.scale_factor
        pygame.draw.circle(
            surface=self.window,
            color=color,
            center=self.to_display(center),
            radius=radius,
            width=width,
        )

    def draw_poly(
        self,
        *,
        color: Color,
        closed: bool = False,
        points: list[Vector2],
    ) -> None:
        """Draw a closed polygon on the `View`, in `World` units,
        which are scaled/translated for display.
        """
        pygame.draw.aalines(
            surface=self.window,
            color=color,
            closed=closed,
            points=[self.to_display(p) for p in points],
        )

    def blit(
        self,
        *,
        source: Surface,
        dest: Vector2,
        display_offset: tuple[int, int],
    ) -> None:
        """Blit to the `View`.

        `dest`: `World` units, which are scaled/translated for display.

        `display_offset`: unscaled display units.
        """
        self.window.blit(
            source=source,
            dest=self.to_display(dest) + display_offset,
        )
