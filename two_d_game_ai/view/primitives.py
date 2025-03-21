"""Contains `pygame.draw` calls."""

from collections.abc import Sequence

from pygame import Color, Rect, Surface, Vector2, draw


def draw_line(
    *,
    surface: Surface,
    color: Color,
    start_pos: Vector2,
    end_pos: Vector2,
    width: int = 1,
    anti_alias: bool = True,
) -> None:
    """Draw a line."""
    if anti_alias and width == 1:
        draw.aaline(surface=surface, color=color, start_pos=start_pos, end_pos=end_pos)

    else:
        # pygame.draw.aaline() only draws single-pixel width lines
        draw.line(
            surface=surface,
            color=color,
            start_pos=start_pos,
            end_pos=end_pos,
            width=width,
        )


def draw_rect(
    *,
    surface: Surface,
    color: Color,
    rect: Rect,
    width: int = 0,
) -> None:
    """Draw a rectangle."""
    draw.rect(surface=surface, color=color, rect=rect, width=width)


def draw_circle(
    *,
    surface: Surface,
    color: Color,
    center: Vector2,
    radius: float,
    width: int = 0,
) -> None:
    """Draw a circle."""
    draw.circle(surface=surface, color=color, center=center, radius=radius, width=width)


def draw_poly(
    *,
    surface: Surface,
    color: Color,
    closed: bool = False,
    points: Sequence[Vector2],
) -> None:
    """Draw a closed polygon."""
    draw.aalines(surface=surface, color=color, closed=closed, points=points)


def blit(
    *,
    source: Surface,
    surface: Surface,
    dest: Vector2,
) -> None:
    """Blit."""
    surface.blit(source=source, dest=dest)
