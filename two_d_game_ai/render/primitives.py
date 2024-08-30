"""Module containing rendering primitives, wrapping `Pygame.draw` functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from two_d_game_ai.render import to_display_radians

if TYPE_CHECKING:
    from pygame import Color, Surface

    from two_d_game_ai import Vector2
    from two_d_game_ai.render.view import View


def draw_circle(
    view: View,
    color: Color,
    center: Vector2,
    radius: float,
) -> None:
    """Draw a circle on the `View`."""
    pygame.draw.circle(
        surface=view.window,
        color=color,
        center=center,
        radius=radius,
    )


def draw_scaled_circle(
    view: View,
    color: Color,
    center: Vector2,
    radius: float,
) -> None:
    """Draw a circle on the `View`, in `World` units,
    which are scaled/translated for display.
    """
    pygame.draw.circle(
        surface=view.window,
        color=color,
        center=view.to_display(center),
        radius=radius * view.scale_factor,
    )


def draw_scaled_circular_arc(
    view: View,
    color: Color,
    center: Vector2,
    radius: int,
    start_angle: float,
    stop_angle: float,
    width: int = 1,
) -> None:
    """Draw a circular arc on the `View`, in `World` units,
    which are scaled/translated for display.

    `width`: unscaled display units.
    """
    enclosing_rect_dimension = int(2 * radius * view.scale_factor)
    enclosing_rect = Rect(0, 0, enclosing_rect_dimension, enclosing_rect_dimension)
    display_center = view.to_display(center)
    # Pygame.Rect requires integer coordinates; draw.arc call does not accept Frect
    enclosing_rect.center = int(display_center.x), int(display_center.y)

    pygame.draw.arc(
        surface=view.window,
        color=color,
        rect=enclosing_rect,
        start_angle=to_display_radians(stop_angle),
        stop_angle=to_display_radians(start_angle),
        width=width,
    )


def draw_scaled_line(
    view: View,
    color: Color,
    start_pos: Vector2,
    end_pos: Vector2,
    width: int = 1,
) -> None:
    """Draw a line on the `View`, in `World` units,
    which are scaled/translated for display.

    `width`: unscaled display units.
    """
    pygame.draw.line(
        surface=view.window,
        color=color,
        start_pos=view.to_display(start_pos),
        end_pos=view.to_display(end_pos),
        width=width,
    )


def draw_scaled_blit(
    view: View,
    source: Surface,
    dest: Vector2,
    display_offset: tuple[int, int],
) -> None:
    """Blit to the `View`.

    `dest`: `World` units, which are scaled/translated for display.

    `display_offset`: unscaled display units.
    """
    view.window.blit(
        source=source,
        dest=view.to_display(dest) + display_offset,
    )
