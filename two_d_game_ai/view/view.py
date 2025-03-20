"""Module containing `View` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Clock, Color, Font, Rect, Surface, Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.observer_pattern import Observer
from two_d_game_ai.view import FONT_SIZE, colors
from two_d_game_ai.view.bot_renderer import BotRenderer
from two_d_game_ai.view.movement_block_renderer import MovementBlockRenderer
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.world.grid_ref import GridRef
    from two_d_game_ai.world.world import World

_PRIMARY_MOUSE_BUTTON = 1
_SECONDARY_MOUSE_BUTTON = 3

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class View(Observer):
    """Renders a `two_d_game_ai.world.world.World` to a window.

    NB: Unlike Pygame default, origin at centre, positive y upwards.
    """

    CAPTION: ClassVar[str] = "2dGameAI"
    MAX_RENDER_FPS: ClassVar = SIMULATION_FPS

    world: World
    """The `World` to be rendered."""
    name: str
    scale_factor: float = 1
    """Scale factor applied to the `World`."""
    margin: int = 0

    running: bool = field(init=False)
    """Flag to control e.g. input handling."""
    window: Surface = field(init=False)
    """Top level Pygame `Surface`."""
    font: Font = field(init=False)
    clock: Clock = field(init=False)
    world_max: float = field(init=False)
    display_offset: Vector2 = field(init=False)
    entity_renderers: dict[int, BotRenderer | MovementBlockRenderer] = field(
        default_factory=dict
    )
    """Maps entity `id` to Renderer."""
    selected: None | MovementBlockRenderer | BotRenderer = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        pygame.init()
        self.font = Font(None, FONT_SIZE)
        _window_size = self.world.size * self.scale_factor + 2 * self.margin
        self.window = pygame.display.set_mode((_window_size, _window_size))
        pygame.display.set_caption(self.CAPTION)
        self.clock = Clock()
        self.running = True

        self.world_max = self.world.size / 2
        self.display_offset = Vector2(
            self.world_max,
            self.world_max,
        ) * self.scale_factor + Vector2(
            self.margin,
            self.margin,
        )
        self.selected = None

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def bot_renderers(self) -> set[BotRenderer]:
        """TO DO."""
        return {r for r in self.entity_renderers.values() if isinstance(r, BotRenderer)}

    @property
    def movement_block_renderers(self) -> set[MovementBlockRenderer]:
        """TO DO."""
        return {
            r
            for r in self.entity_renderers.values()
            if isinstance(r, MovementBlockRenderer)
        }

    @property
    def clickables(self) -> set[BotRenderer | MovementBlockRenderer]:
        """Clickable elements."""
        return set(self.entity_renderers.values())

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

    def render(self) -> None:
        """Render the `World` to the Pygame window."""
        # Limit update rate to save CPU:
        self.clock.tick(self.MAX_RENDER_FPS)

        self._ensure_renderers()
        # Drawn in order, bottom layer to top:
        self.window.fill(colors.WINDOW_FILL)
        self._draw_world_limits()
        self._draw_grid()
        for b in self.bot_renderers:
            b.draw()
        for m in self.movement_block_renderers:
            m.draw()
        self._draw_axes()

        self._draw_step_counter()
        # update entire display
        pygame.display.flip()

    def _ensure_renderers(self) -> None:
        for m in self.world.movement_blocks:
            if m.id not in self.entity_renderers:
                self.entity_renderers[m.id] = MovementBlockRenderer(view=self, entity=m)
                log_msg = f"{m.name} renderer added."
                logger.debug(log_msg)
        for b in self.world.bots:
            if b.id not in self.entity_renderers:
                b.register_observer(self)
                self.entity_renderers[b.id] = BotRenderer(view=self, entity=b)
                log_msg = f"{b.name} renderer added."
                logger.debug(log_msg)

    def _handle_mouse_select(self, click_pos: Vector2) -> None:
        self.selected = self._clicked_entity(click_pos)
        for renderer in self.clickables:
            renderer.is_selected = renderer == self.selected

    def _clicked_entity(
        self, click_pos: Vector2
    ) -> MovementBlockRenderer | BotRenderer | None:
        """Return the EntityRenderer at click position, or None."""
        for renderer in self.clickables:
            if renderer.is_clicked(click_pos):
                log_msg = f"{renderer.entity.name} clicked."
                logger.debug(log_msg)
                return renderer
        return None

    def _handle_mouse_set_destination(self, click_pos: Vector2) -> None:
        """Attempt to set destination, if applicable to current selection."""
        clicked_grid_ref = self._clicked_grid_ref(click_pos)
        if (
            isinstance(self.selected, BotRenderer)
            and isinstance(self.selected.entity, Bot)
            and self.world.grid.is_traversable(clicked_grid_ref)
        ):
            self.selected.entity.destination = self._to_world(click_pos)

    def _clicked_grid_ref(self, click_pos: Vector2) -> GridRef:
        """Return the GridRef at click position, or None."""
        return Grid.cell_from_world_pos(self.world, self._to_world(click_pos))

    def _draw_world_limits(self) -> None:
        """Draw the `World` limits."""
        # Border
        self.draw_rect(
            color=colors.WORLD_FILL,
            rect=Rect(
                (-self.world_max, -self.world_max),
                (self.world.size, self.world.size),
            ),
        )

    def _draw_axes(self) -> None:
        self.draw_line(  # Y
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(0, -self.world_max),
            end_pos=Vector2(0, self.world_max),
        )
        self.draw_line(  # X
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(-self.world_max, 0),
            end_pos=Vector2(self.world_max, 0),
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
                start_pos=Vector2(-self.world_max, cell_offset),
                end_pos=Vector2(self.world_max, cell_offset),
                width=1,
                anti_alias=False,
            )
            # vertical grid line
            self.draw_line(
                color=colors.WORLD_GRID_LINE,
                start_pos=Vector2(cell_offset, -self.world_max),
                end_pos=Vector2(cell_offset, self.world_max),
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

        text_content = [
            f"sim elapsed: {elapsed_time:.1f} s",
            f"sim step: {self.world.step_counter}",
        ]
        if self.world.is_paused:
            text_content.append("paused")
        text = self.font.render(
            text="\n".join(text_content),
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
            world_pos.reflect(Vector2(0, 1)) * self.scale_factor + self.display_offset
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
        pos = (display_pos - self.display_offset) / self.scale_factor
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
        points: Sequence[Vector2],
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
