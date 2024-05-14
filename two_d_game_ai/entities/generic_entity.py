"""Generic entity class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S, Vector2
from two_d_game_ai.entities.observer_pattern import _Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class _GenericEntity(_Subject, ABC):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    name: str
    pos: tuple[float, float] | None
        Position (World coordinates)
    pos_v: Vector2
        Position (World coordinates)
    world: World
    """

    def __init__(self, world: World, name: str, pos: tuple[float, float]) -> None:
        super().__init__(name)
        self.world = world
        self.pos = pos
        self.pos_v = Vector2(pos)
        self._velocity_v = Vector2(0, 0)

    @abstractmethod
    def update(self, *args: Any) -> None:
        """Update entity over 1 simulation step."""
        self._move()

    def _move(self) -> None:
        """Change position over 1 simulation step."""
        self.pos_v += self._velocity_v * SIMULATION_STEP_INTERVAL_S

    def stop(self) -> None:
        """Stop."""
        self._velocity_v = Vector2(0)
