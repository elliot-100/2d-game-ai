"""Package implementing Observer pattern."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from two_d_game_ai.world.world import World


logger = logging.getLogger(__name__)

ObserverException = Exception


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
    observers: set[Observer] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.id = len(self.world.entities)
        log_msg = f"Subject '{self.name}' initiated."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return hash(self.id)

    def register_observer(self, observer: Observer) -> None:
        """Register an observer."""
        self.observers.add(observer)
        log_msg = f"Observer '{observer.name}' registered with Subject '{self.name}'."
        logger.debug(log_msg)

    def unregister_observer(self, observer: Observer) -> None:
        """Unregister a observer."""
        self.observers.discard(observer)
        log_msg = f"Observer '{observer.name}' unregistered from Subject '{self.name}'."
        logger.debug(log_msg)

    def notify_observers(self, message: str) -> None:
        """Send a message to all observers."""
        log_msg = f"Subject '{self.name}' notifying observers: '{message}'."
        logger.debug(log_msg)
        if self.observers:
            for observers in self.observers:
                observers.report_event(message, self)
        else:
            error_msg = f"Subject '{self.name}' has no observers."
            raise ObserverException(error_msg)


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
        log_msg = f"Observer '{self.name}' initiated."
        logger.debug(log_msg)

    def __hash__(self) -> int:
        return hash(self._id)

    def report_event(self, message: str, sender: Subject) -> None:
        """Report the received message.

        Don't need to call this explicitly, it's called by Subject.dispatch().
        """
        log_msg = f"Observer '{self.name}' got '{message}' from '{sender.name}'."
        logger.debug(log_msg)
