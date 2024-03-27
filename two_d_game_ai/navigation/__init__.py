"""Basic Cartesian navigation functions wrapped around Pygame.Vector2 library.

Coordinates have positive y-axis upwards, i.e. North at (0, 1).
Bearings (aka azimuthal angle) in positive degrees clockwise from North.

Pygame coordinates, like most graphics systems, have positive y-axis downwards,
i.e. North at (0, -1).
"""

from pygame import Vector2


def point_in_or_on_circle(
    point: Vector2,
    circle_centre: Vector2,
    circle_radius: float,
) -> bool:
    """Determine if a point is (inside or on) a circle.

    Parameters
    ----------
    point
    circle_centre
    circle_radius

    Returns
    -------
    bool
        True if the point is (inside or on) the circle
    """
    return (point - circle_centre).length() <= circle_radius
