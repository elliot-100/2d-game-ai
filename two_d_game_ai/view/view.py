"""Contains `View` class."""

from __future__ import annotations

import logging
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Clock, Font, Surface, Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.view import FONT_SIZE, colors
from two_d_game_ai.view.world_renderer import WorldRenderer

if TYPE_CHECKING:
    from two_d_game_ai.world.world import World

_PRIMARY_MOUSE_BUTTON = 1
_SECONDARY_MOUSE_BUTTON = 3
_PAUSE_KEY = pygame.K_p

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class View:
    """Renders the simulation to a window."""

    CAPTION: ClassVar[str] = "2dGameAI"
    MAX_RENDER_FPS: ClassVar = SIMULATION_FPS
    MARGIN: ClassVar[int] = 20

    world: World
    """The `World` to be rendered."""
    world_renderer_name: InitVar[str] = "UNNAMED WORLD_RENDERER"
    """Passed to `self.world_renderer`."""
    scale_factor: float = 1
    """Scale factor applied to the `World` render."""
    show_debug_while_unpaused: bool = False

    running: bool = field(init=False)
    """Flag to control e.g. input handling."""
    window: Surface = field(init=False)
    """The top level pygame `Surface`."""
    world_renderer: WorldRenderer = field(init=False)
    """Delegated `World` renderer."""
    font: Font = field(init=False)
    clock: Clock = field(init=False)

    def __post_init__(self, world_renderer_name: str) -> None:
        pygame.init()
        self.font = Font(None, FONT_SIZE)
        world_render_size = self.world.size * self.scale_factor
        window_size = world_render_size + 2 * self.MARGIN
        self.window = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption(self.CAPTION)
        self.world_renderer = WorldRenderer(
            world=self.world,
            scale_factor=self.scale_factor,
            name=world_renderer_name,
        )
        self.clock = Clock()
        self.running = True

    def __hash__(self) -> int:
        return super().__hash__()

    def handle_inputs(self) -> None:
        """Handle user inputs."""
        for event in pygame.event.get():
            match event.type:
                # WINDOW/HIGH LEVEL EVENTS
                case pygame.QUIT:  # user clicked window close
                    self.running = False

                # MOUSE EVENTS
                case pygame.MOUSEBUTTONDOWN:
                    world_panel_click_pos = Vector2(event.pos) - Vector2(
                        self.MARGIN, self.MARGIN
                    )
                    if event.button == _PRIMARY_MOUSE_BUTTON:
                        self.world_renderer.handle_mouse_select(world_panel_click_pos)
                    elif event.button == _SECONDARY_MOUSE_BUTTON:
                        self.world_renderer.handle_mouse_set_destination(
                            world_panel_click_pos
                        )

                # KEYBOARD EVENTS
                case pygame.KEYDOWN:
                    if event.key == _PAUSE_KEY:
                        self.world.is_paused = not self.world.is_paused

    def render(self) -> None:
        """Render to the Pygame window."""
        # Limit update rate to save CPU:
        self.clock.tick(self.MAX_RENDER_FPS)
        self.window.fill(colors.WINDOW_FILL)
        if self.world.is_paused or self.show_debug_while_unpaused:
            self.world_renderer.render(debug_render_mode=True)
        else:
            self.world_renderer.render()
        self.window.blit(
            source=self.world_renderer.surface, dest=(self.MARGIN, self.MARGIN)
        )
        self._draw_step_counter()
        # update entire display
        pygame.display.flip()

    def _draw_step_counter(self) -> None:
        """Render the step counter and blit to window."""
        elapsed_time = self.world.step_counter / SIMULATION_FPS

        text_content = [
            f"sim elapsed: {elapsed_time:.1f} s",
            f"sim step: {self.world.step_counter}",
            f"entity renderers: {len(self.world_renderer.entity_renderers)}",
        ]
        if self.world.is_paused:
            text_content.append("paused")
        text = self.font.render(
            text="\n".join(text_content),
            antialias=True,
            color=colors.WINDOW_TEXT,
        )
        self.window.blit(source=text)
