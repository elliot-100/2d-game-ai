"""Contains `WorldRenderer` class."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from loguru import logger
from pygame import Color, Font, Rect, Surface, Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import is_obstacle
from two_d_game_ai.view import FONT_DIR_RELATIVE, FONT_FILENAME, FONT_SIZE, colors
from two_d_game_ai.view.bot_renderer import BotRenderer
from two_d_game_ai.view.obstacle_renderers import ObstacleRenderer
from two_d_game_ai.view.primitives import (
    blit,
    draw_circle,
    draw_line,
    draw_poly,
    draw_rect,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer
    from two_d_game_ai.world.grid import Grid
    from two_d_game_ai.world.world import World


@dataclass(kw_only=True)
class WorldRenderer:
    """Renders the `World` to the `view`.

    NB: Unlike Pygame default, origin at centre, positive y upwards.
    """

    GRID_NODE_RADIUS: ClassVar[int] = 1
    """Display units."""

    world: World
    """The `World` to be rendered."""
    scale_factor: float
    """Scale factor applied to the render."""
    name: str = ""
    size: float = field(init=False)
    """Display units."""
    surface: Surface = field(init=False)
    """pygame `Surface`."""
    entity_renderers: dict[int, GenericEntityRenderer] = field(default_factory=dict)
    """Maps entity `id` to delegated renderer."""
    selected_renderer: GenericEntityRenderer | None = field(init=False)
    """Selected entity renderer."""
    font: Font = field(init=False)

    def __post_init__(self) -> None:
        font_filepath = Path(__file__).resolve().parent / FONT_DIR_RELATIVE
        self.font = Font(font_filepath / FONT_FILENAME, FONT_SIZE)
        self.size = self.world.size * self.scale_factor
        self.surface = Surface((self.size, self.size))
        self.base_grid_surface = self.base_grid()
        self.selected_renderer = None
        logger.info(f"WorldRenderer(size={self.size}) initialized.")

    def __hash__(self) -> int:
        return hash(self.name)
        # TO DO: fragile!

    def __str__(self) -> str:
        """Human-readable description."""
        return f"{type(self).__name__}"

    @property
    def bot_renderers(self) -> set[BotRenderer]:
        """TO DO."""
        return {r for r in self.entity_renderers.values() if isinstance(r, BotRenderer)}

    @property
    def obstacle_renderers(self) -> set[ObstacleRenderer]:
        """TO DO."""
        return {
            r for r in self.entity_renderers.values() if isinstance(r, ObstacleRenderer)
        }

    @property
    def clickables(self) -> set[GenericEntityRenderer]:
        """Clickable elements."""
        return set(self.entity_renderers.values())

    def render(self, *, debug_render_mode: bool = False) -> None:
        """Render the `World` to `self.surface`."""
        self.ensure_renderers()
        # Drawn in order, bottom layer to top:
        self.surface.blit(self.base_grid_surface)
        self.render_movement_blocking_cells(self.world.grid)
        for b in self.bot_renderers:
            b.render(debug_render_mode=debug_render_mode)
        for m in self.obstacle_renderers:
            m.render()
        self.render_axes()

    def base_grid(self) -> Surface:
        """Pre-render grid to a static surface."""
        surface = Surface((self.size, self.size))
        surface.fill(colors.WORLD_FILL)

        cell_size = self.world.grid_resolution
        cell_offsets = [
            cell_size * i - self.world.magnitude + cell_size / 2
            for i in range(self.world.grid.size)
        ]
        for x, y in itertools.product(cell_offsets, cell_offsets):
            self.draw_circle(
                surface=surface,
                color=colors.WORLD_GRID_LINE,
                center=Vector2(x, y),
                radius=self.GRID_NODE_RADIUS,
                scale_radius=False,
            )
        return surface

    def ensure_renderers(self) -> None:
        """Update the set of entity renderers."""
        for e in {e for e in self.world.entities if e.id not in self.entity_renderers}:
            if e.id is None:
                err_msg = f"{e!s} must have an `id` to be rendered."
                raise ValueError(err_msg)

            if is_obstacle(e):
                self.entity_renderers[e.id] = ObstacleRenderer(parent=self, entity=e)
            elif isinstance(e, Bot):
                self.entity_renderers[e.id] = BotRenderer(parent=self, entity=e)
            logger.debug(f"Added renderer for {e!s}.")

    def to_local(self, world_pos: Vector2) -> Vector2:
        """Convert `World` coordinates to local coordinates.

        Parameters
        ----------
        world_pos
            `World` coordinates

        Returns
        -------
        Vector2
            Local coordinates.
            Origin is at centre, positive y upwards.
        """
        pos = world_pos
        pos = pos.elementwise() * Vector2(1, -1)
        offset = self.world.magnitude
        pos += Vector2(offset, offset)
        return pos * self.scale_factor

    def to_world(self, local_pos: Vector2) -> Vector2:
        """Convert local coordinates to `World` coordinates.

        Parameters
        ----------
        local_pos
            Local coordinates.
            Origin is at centre, positive y upwards.

        Returns
        -------
        Vector2
            `World` coordinates.
        """
        pos = local_pos / self.scale_factor
        offset = self.world.magnitude
        pos -= Vector2(offset, offset)
        return pos.elementwise() * Vector2(1, -1)

    def render_movement_blocking_cells(self, grid: Grid) -> None:
        """Fill the cells within obstacles."""
        cell_size = self.world.grid_resolution
        for cell_ref in grid.movement_blocking_cells:
            grid_rect = Rect(
                (cell_ref.x * cell_size, cell_ref.y * cell_size), (cell_size, cell_size)
            )
            # draw slightly oversize to avoid antialiasing issues
            grid_rect = grid_rect.move(-0.5, -0.5)
            grid_rect.width += 1
            grid_rect.height += 1
            self.draw_rect(color=colors.OBSTACLE_FILL, rect=Rect(grid_rect), width=0)

    def render_axes(self) -> None:
        """Draw axes."""
        self.draw_line(
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(0, -self.world.magnitude),
            end_pos=Vector2(0, self.world.magnitude),
        )
        self.draw_line(
            color=colors.WORLD_AXES_LINE,
            start_pos=Vector2(-self.world.magnitude, 0),
            end_pos=Vector2(self.world.magnitude, 0),
        )

    def handle_mouse_select(self, local_pos: Vector2) -> None:
        """TO DO."""
        self.selected_renderer = self.entity_renderer_at_pos(local_pos)
        for renderer in self.clickables:
            renderer.is_selected = renderer == self.selected_renderer

    def entity_renderer_at_pos(self, pos: Vector2) -> GenericEntityRenderer | None:
        """Return the EntityRenderer at position, or None."""
        for renderer in self.clickables:
            if renderer.is_clicked(pos):
                logger.debug(f"{renderer!s}: clicked.")
                return renderer
        return None

    def handle_mouse_set_destination(self, local_pos: Vector2) -> Vector2 | None:
        """Attempt to set destination, if applicable to current selection."""
        if not isinstance(self.selected_renderer, BotRenderer):
            return None  # Only `Bot`s support destination setting

        if not isinstance(self.selected_renderer.entity, Bot):
            raise TypeError

        world_pos = self.to_world(local_pos)
        if self.world.location_is_movement_blocked(world_pos):
            return None

        self.selected_renderer.entity.destination = world_pos
        return world_pos

    def draw_line(
        self,
        *,
        color: Color,
        start_pos: Vector2,
        end_pos: Vector2,
        width: int = 1,
    ) -> None:
        """Draw a line in `World` units on `self.surface`.

        `width`: display pixels.
        """
        draw_line(
            surface=self.surface,
            color=color,
            start_pos=self.to_local(start_pos),
            end_pos=self.to_local(end_pos),
            width=width,
        )

    def draw_polyline(
        self,
        *,
        color: Color,
        points: Sequence[Vector2],
        width: int = 1,
    ) -> None:
        """Draw a polyline in `World` units on `self.surface`.

        `width`: display pixels.
        """
        point_pairs = itertools.pairwise(points)
        for start_pos, end_pos in point_pairs:
            draw_line(
                surface=self.surface,
                color=color,
                start_pos=self.to_local(start_pos),
                end_pos=self.to_local(end_pos),
                width=width,
            )

    def draw_rect(
        self,
        *,
        color: Color,
        rect: Rect,
        width: int = 0,
    ) -> None:
        """Draw a rectangle in `World` units on `self.surface`.

        `width`: display pixels.

        """
        scaled_pos = self.to_local(Vector2(rect.left, rect.top))
        scaled_width = rect.width * self.scale_factor
        scaled_height = rect.height * self.scale_factor
        draw_rect(
            surface=self.surface,
            color=color,
            rect=Rect(
                # TODO: transform rect?
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
        surface: Surface,  # TODO: why does this draw method have this param?
        color: Color,
        center: Vector2,
        radius: float,
        width: int = 0,
        scale_radius: bool = True,
    ) -> None:
        """Draw a circle in `World` units on a surface.

        Optionally supress radius scaling e.g. for icons whose size is independent
        of view scaling.

        `width`: display pixels.
        """
        if scale_radius:
            radius *= self.scale_factor
        draw_circle(
            surface=surface,
            color=color,
            center=self.to_local(center),
            radius=radius,
            width=width,
        )

    def draw_poly(
        self,
        *,
        color: Color,
        closed: bool,
        points: Sequence[Vector2],
    ) -> None:
        """Draw an unfilled 1 px anti-aliased polygon/polyline in `World` units
        on `self.surface`.
        """
        draw_poly(
            surface=self.surface,
            color=color,
            closed=closed,
            points=[self.to_local(p) for p in points],
        )

    def draw_pie(
        self,
        *,
        color: Color,
        center: Vector2,
        radius: float,
        central_angle: float,
        theta: float,
    ) -> None:
        """Draw a closed unfilled pie wedge in `World` units on `self.surface`."""
        angle_step_degrees = 5
        draw_angles = [
            *list(range(0, int(theta), angle_step_degrees)),
            theta,  # so theta is always drawn, irrespective of step
        ]
        offsets = [
            Vector2(0, radius).rotate(
                theta / 2
                - angle
                - central_angle,  # Pygame rotates CCW, thus negative angle
            )
            for angle in draw_angles
        ]
        self.draw_poly(
            color=color,
            closed=True,
            points=[center] + [center + offset for offset in offsets],
        )

    def blit(
        self,
        *,
        source: Surface,
        dest: Vector2 | None = None,
        display_offset: Vector2 | None = None,
    ) -> None:
        """Blit to `self.surface`.

        `dest`: `World` units, which are scaled/translated for display.

        `display_offset`: unscaled display units.
        """
        if dest is None:
            dest = Vector2(0, 0)
        if display_offset is None:
            display_offset = Vector2(0, 0)
        blit(
            source=source,
            surface=self.surface,
            dest=self.to_local(dest) + display_offset,
        )
