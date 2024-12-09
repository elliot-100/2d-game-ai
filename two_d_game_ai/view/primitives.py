"""Module containing rendering primitives, wrapping `Pygame.draw` functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Vector2

if TYPE_CHECKING:
    from pygame import Color, Surface

    from two_d_game_ai.view.view import View


def draw_circle(
    view: View,
    color: Color,
    center: Vector2,
    radius: float,
    width: int = 0,
) -> None:
    """Draw a circle on the `View`."""
    pygame.draw.aacircle(
        surface=view.window,
        color=color,
        center=center,
        radius=radius,
        width=width,
    )


def draw_scaled_circle(
    view: View,
    color: Color,
    center: Vector2,
    radius: float,
    width: int = 0,
    *,
    scale_radius: bool = True,
) -> None:
    """Draw a circle on the `View`, in `World` units, which are scaled/translated for
    display. Optionally supress radius scaling e.g. for icons whose size is independent
    of view scaling.
    """
    if scale_radius:
        radius *= view.scale_factor
    draw_circle(
        view=view,
        color=color,
        center=view.to_display(center),
        radius=radius,
        width=width,
    )


def draw_scaled_line(
    view: View,
    color: Color,
    start_pos: Vector2,
    end_pos: Vector2,
    width: int = 1,
    *,
    anti_alias: bool = True,
) -> None:
    """Draw a line on the `View`, in `World` units,
    which are scaled/translated for display.

    `width`: unscaled display units.
    """
    if anti_alias and width == 1:
        pygame.draw.aaline(
            surface=view.window,
            color=color,
            start_pos=view.to_display(start_pos),
            end_pos=view.to_display(end_pos),
        )

    else:
        # pygame.draw.aaline() only draws single-pixel width lines
        pygame.draw.line(
            surface=view.window,
            color=color,
            start_pos=view.to_display(start_pos),
            end_pos=view.to_display(end_pos),
            width=width,
        )


def draw_scaled_rect(
    view: View,
    color: Color,
    rect: Rect,
    width: int,
) -> None:
    """Draw a rectangle on the `View`, in `World` units,
    which are scaled/translated for display.

    `width`: unscaled display units.
    """
    scaled_pos = view.to_display(Vector2(rect.left, rect.top))
    scaled_width = rect.width * view.scale_factor
    scaled_height = rect.height * view.scale_factor
    pygame.draw.rect(
        surface=view.window,
        color=color,
        rect=(
            scaled_pos.x,
            scaled_pos.y - scaled_height,
            scaled_width,
            scaled_height,
        ),
        width=width,
    )


def draw_scaled_poly(
    view: View,
    color: Color,
    points: list[Vector2],
) -> None:
    """Draw a closed polygon on the `View`, in `World` units,
    which are scaled/translated for display.
    """
    pygame.draw.aalines(
        surface=view.window,
        color=color,
        closed=True,
        points=[view.to_display(p) for p in points],
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
