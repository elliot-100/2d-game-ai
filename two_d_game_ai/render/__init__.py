"""Package for rendering the model using Pygame."""

from __future__ import annotations

from math import radians


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
    return radians(-bearing_deg + 90)
