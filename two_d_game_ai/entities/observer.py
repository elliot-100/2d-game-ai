"""Contains `Observer` class."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from two_d_game_ai.entities.subject import Subject
    from two_d_game_ai.world.world import World


logger = logging.getLogger(__name__)

ObserverException = Exception


@dataclass
class Observer:
    """Observer class.

    Viewers (e.g. renderers) inherit from this class.
    """

    world: World
    """Reference to `World` object."""
    name: str
    _id: int = field(init=False)

    def __post_init__(self) -> None:
        self._id = len(self.world.entities)
        log_msg = f"Observer '{self.name}' initialised."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return hash(self._id)

    def report_event(self, message: str, sender: Subject) -> None:
        """Report the received message.

        Don't need to call this explicitly; it's called by `Subject.dispatch()`.
        """
        log_msg = f"Observer '{self.name}' got '{message}' from '{sender.name}'."
        logger.debug(log_msg)
