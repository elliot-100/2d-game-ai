"""Contains `Subject` class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from two_d_game_ai.entities.observer import Observer, ObserverException, logger

if TYPE_CHECKING:
    from two_d_game_ai.world.world import World


@dataclass(kw_only=True)
class Subject:
    """Subject (a.k.a. Observable) class.

    All simulated entity classes inherit from this class.
    """

    id: int = field(init=False)
    """Used as hash value."""
    world: World
    """Reference to `World` object."""
    name: str
    observers: set[Observer] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.id = len(self.world.entities)
        # TODO: fragile, assumes is about to be added to `self.world.entities`
        log_msg = f"Subject '{self.name}' initialised."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return hash(self.id)

    def register_observer(self, observer: Observer) -> None:
        """Register an `Observer`."""
        self.observers.add(observer)
        log_msg = f"Observer '{observer.name}' registered with Subject '{self.name}'."
        logger.debug(log_msg)

    def unregister_observer(self, observer: Observer) -> None:
        """Unregister an `Observer`."""
        self.observers.discard(observer)
        log_msg = f"Observer '{observer.name}' unregistered from Subject '{self.name}'."
        logger.debug(log_msg)

    def notify_observers(self, message: str) -> None:
        """Send a message to all `Observer`s."""
        log_msg = f"Subject '{self.name}' notifying observers: '{message}'."
        logger.debug(log_msg)
        if self.observers:
            for observers in self.observers:
                observers.report_event(message, self)
        else:
            error_msg = f"Subject '{self.name}' has no observers."
            raise ObserverException(error_msg)
