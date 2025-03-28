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
) -> None:
    """Draw a line. Anti-aliased if `width` is 1."""
    if width == 1:
        draw.aaline(surface=surface, color=color, start_pos=start_pos, end_pos=end_pos)

    else:
        # pygame.draw.aaline() has poor quality for width > 1
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
    """Draw an anti-aliased circle."""
    draw.aacircle(
        surface=surface, color=color, center=center, radius=radius, width=width
    )


def draw_poly(
    *,
    surface: Surface,
    color: Color,
    points: Sequence[Vector2],
) -> None:
    """Draw a closed anti-aliased polygon."""
    draw.aalines(surface=surface, color=color, closed=True, points=points)


def blit(
    *,
    source: Surface,
    surface: Surface,
    dest: Vector2,
) -> None:
    """Blit."""
    surface.blit(source=source, dest=dest)
