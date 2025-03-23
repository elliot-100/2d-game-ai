"""Contains `WorldRenderer` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Color, Rect, Surface, Vector2

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view import colors
from two_d_game_ai.view.bot_renderer import BotRenderer
from two_d_game_ai.view.movement_block_renderer import MovementBlockRenderer
from two_d_game_ai.view.primitives import (
    blit,
    draw_circle,
    draw_line,
    draw_poly,
    draw_rect,
)
from two_d_game_ai.world.grid import Grid

if TYPE_CHECKING:
    from collections.abc import Sequence

    from two_d_game_ai.view.generic_entity_renderer import GenericEntityRenderer
    from two_d_game_ai.world.world import World

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class WorldRenderer:
    """Renders the `World` to the `view`.

    NB: Unlike Pygame default, origin at centre, positive y upwards.
    """

    world: World
    """The `World` to be rendered."""
    scale_factor: float = 1
    """Scale factor applied to the render."""
    name: str = "UNNAMED WORLD_RENDERER"

    surface: Surface = field(init=False)
    """pygame `Surface`."""
    entity_renderers: dict[int, GenericEntityRenderer] = field(default_factory=dict)
    """Maps entity `id` to delegated renderer."""
    selected_renderer: GenericEntityRenderer | None = field(init=False)
    """Selected entity renderer."""

    def __post_init__(self) -> None:
        scaled_world_size = self.world.size * self.scale_factor
        self.surface = Surface((scaled_world_size, scaled_world_size))
        self.selected_renderer = None
        log_msg = f"WorldRenderer '{self.name}' initiated."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return hash(self.name)
        # TO DO: fragile!

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
    def clickables(self) -> set[GenericEntityRenderer]:
        """Clickable elements."""
        return set(self.entity_renderers.values())

    def render(self, *, debug_render_mode: bool = False) -> None:
        """Render the `World` to `self.surface`."""
        self.ensure_renderers()
        # Drawn in order, bottom layer to top:
        self.surface.fill(colors.WORLD_FILL)
        self.render_base_grid(self.world.grid)
        self.render_untraversable_cells(self.world.grid)
        for b in self.bot_renderers:
            b.draw(debug_render_mode=debug_render_mode)
        for m in self.movement_block_renderers:
            m.draw()
        self.render_axes()

    def ensure_renderers(self) -> None:
        """Update the set of entity renderers."""
        for e in self.world.entities:
            if e.id not in self.entity_renderers:
                if isinstance(e, MovementBlock):
                    self.entity_renderers[e.id] = MovementBlockRenderer(
                        world_renderer=self, entity=e
                    )
                elif isinstance(e, Bot):
                    self.entity_renderers[e.id] = BotRenderer(
                        world_renderer=self, entity=e
                    )
                log_msg = f"{e.name} renderer added."
                logger.debug(log_msg)

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

    def render_base_grid(self, grid: Grid) -> None:
        """Draw the `Grid`."""
        cell_size = self.world.grid_resolution

        for cell_index in range(grid.size + 1):
            cell_offset = cell_size * (cell_index - grid.size / 2)
            # horizontal grid line
            self.draw_line(
                color=colors.WORLD_GRID_LINE,
                start_pos=Vector2(-self.world.magnitude, cell_offset),
                end_pos=Vector2(self.world.magnitude, cell_offset),
                width=1,
                anti_alias=False,
            )
            # vertical grid line
            self.draw_line(
                color=colors.WORLD_GRID_LINE,
                start_pos=Vector2(cell_offset, -self.world.magnitude),
                end_pos=Vector2(cell_offset, self.world.magnitude),
                width=1,
                anti_alias=False,
            )

    def render_untraversable_cells(self, grid: Grid) -> None:
        """Draw the `Grid`."""
        oversize_px = 2
        cell_size = self.world.grid_resolution

        for cell_ref in grid.untraversable_cells:
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
                color=colors.MOVEMENT_BLOCK_FILL, rect=Rect(oversize_grid_rect), width=0
            )

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
                log_msg = f"{renderer.entity.name} clicked."
                logger.debug(log_msg)
                return renderer
        return None

    def handle_mouse_set_destination(self, local_pos: Vector2) -> Vector2 | None:
        """Attempt to set destination, if applicable to current selection."""
        if not isinstance(self.selected_renderer, BotRenderer):
            return None  # Only `Bot`s support destination setting
        if not isinstance(self.selected_renderer.entity, Bot):
            raise TypeError
        world_pos = self.to_world(local_pos)
        cell = Grid.cell_from_world_pos(world=self.world, pos=world_pos)
        if not self.world.grid.is_traversable(cell):
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
        anti_alias: bool = True,
    ) -> None:
        """Draw a line in `World` units.

        `width`: display pixels.
        """
        draw_line(
            surface=self.surface,
            color=color,
            start_pos=self.to_local(start_pos),
            end_pos=self.to_local(end_pos),
            width=width,
            anti_alias=anti_alias,
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
        scaled_pos = self.to_local(Vector2(rect.left, rect.top))
        scaled_width = rect.width * self.scale_factor
        scaled_height = rect.height * self.scale_factor
        draw_rect(
            surface=self.surface,
            color=color,
            rect=Rect(
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
        """Draw a circle in `World` units on `self.surface`.

        Optionally supress radius scaling e.g. for icons whose size is independent
        of view scaling.

        `width`: display pixels.
        """
        if scale_radius:
            radius *= self.scale_factor
        draw_circle(
            surface=self.surface,
            color=color,
            center=self.to_local(center),
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
        """Draw a closed polygon in `World` units on `self.surface`."""
        draw_poly(
            surface=self.surface,
            color=color,
            closed=closed,
            points=[self.to_local(p) for p in points],
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
