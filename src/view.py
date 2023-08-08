"""Renderer using Pygame."""

import pygame
from pygame import Vector2

from src.world import World

BACKGROUND_COLOR = GREY_80 = (51, 51, 51)
FOREGROUND_COLOR = RED = (255, 0, 0)
ICON_RADIUS = 10


class View:
    """The View class.

    Attributes
    ----------
    world
        World to be viewed
    window
        Top level 'display surface'
    """

    def __init__(self, world: World) -> None:
        """Wrap Pygame window initialisation."""
        self.world = world
        self.running = True

        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.window = pygame.display.set_mode((world.radius * 2, world.radius * 2))
        pygame.display.set_caption("2dGameAI")
        self.clock = pygame.Clock()

    def render(self) -> None:
        """Output a representation of the world to the window."""
        # Limit update to 60 FPS
        self.clock.tick(60)
        # render background
        self.window.fill(BACKGROUND_COLOR)
        # render world limits
        pygame.draw.circle(
            self.window,
            FOREGROUND_COLOR,
            self.to_display(Vector2(0, 0)),
            self.world.radius,
            1,
        )
        # render all bots
        for bot in self.world.bots.values():
            pygame.draw.circle(
                self.window,
                FOREGROUND_COLOR,
                self.to_display(bot.pos),
                ICON_RADIUS,
                0,
            )

        text = self.font.render(
            text=f"step: {self.world.step_counter}",
            antialias=True,
            color=FOREGROUND_COLOR,
        )
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
        Window coordinates, with origin at centre

        """
        offset = Vector2(self.world.radius, self.world.radius)
        return world_pos + offset

    def handle_window_close(self) -> None:
        """Wrap Pygame window close handling."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user clicked window close
                self.running = False
