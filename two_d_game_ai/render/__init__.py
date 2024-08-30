"""Package implementing Pygame renderer."""

from __future__ import annotations

from math import radians

from two_d_game_ai.geometry import CIRCLE_DEGREES


def _to_display_radians(bearing_deg: float) -> float:
    """Convert bearing (degrees) to Pygame-compatible angle (radians).

    For use in e.g. calls to `pygame.draw.arc`

    Parameters
    ----------
    bearing_deg
        Conventional bearing angle in degrees CCW from North

    Returns
    -------
    float
        Pygame-compatible angle in radians CW from East

    """
    return radians(-bearing_deg + CIRCLE_DEGREES / 4)
