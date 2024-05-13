"""Low level rendering primitives."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from two_d_game_ai.render import _to_display_radians

if TYPE_CHECKING:
    from pygame import Color, Surface

    from two_d_game_ai import Vector2
    from two_d_game_ai.render.view import View


def _circle(view: View, color: Color, center: Vector2, radius: float) -> None:
    pygame.draw.circle(
        surface=view.window,
        color=color,
        center=center,
        radius=radius,
    )


def _scaled_circular_arc(
    view: View,
    color: Color,
    center: Vector2,
    radius: int,
    start_angle: float,
    stop_angle: float,
    width: int = 1,
) -> None:
    """Draw a circular arc, scaled to display coordinates."""
    enclosing_rect_dimension = int(2 * radius * view.scale_factor)
    enclosing_rect = Rect(0, 0, enclosing_rect_dimension, enclosing_rect_dimension)
    display_center = view.to_display(center)
    # Pygame.Rect requires integer coordinates; draw.arc call does not accept Frect
    enclosing_rect.center = int(display_center.x), int(display_center.y)

    pygame.draw.arc(
        surface=view.window,
        color=color,
        rect=enclosing_rect,
        start_angle=_to_display_radians(stop_angle),
        stop_angle=_to_display_radians(start_angle),
        width=width,
    )


def _scaled_line(
    view: View,
    color: Color,
    start_pos: Vector2,
    end_pos: Vector2,
    width: int = 1,
) -> None:
    pygame.draw.line(
        surface=view.window,
        color=color,
        start_pos=view.to_display(start_pos),
        end_pos=view.to_display(end_pos),
        width=width,
    )


def _scaled_blit(
    view: View,
    source: Surface,
    dest: Vector2,
    display_offset: tuple[int, int],
) -> None:
    view.window.blit(
        source=source,
        dest=view.to_display(dest) + display_offset,
    )
