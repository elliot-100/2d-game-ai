"""Package implementing Observer pattern."""

from __future__ import annotations

import logging

ObserverException = Exception


class Subject:
    """Subject (a.k.a. Observable) class.

    All simulated entity classes inherit from this class.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.observers: set[Observer] = set()
        log_msg = f"Subject `{self.name}` initiated"
        logging.info(log_msg)

    def register_observer(self, observer: Observer) -> None:
        """Register an observer."""
        self.observers.add(observer)
        log_msg = f"Observer `{observer.name}` registered with Subject `{self.name}`"
        logging.info(log_msg)

    def unregister_observer(self, observer: Observer) -> None:
        """Unregister a observer."""
        self.observers.discard(observer)
        log_msg = f"Observer `{observer.name}` unregistered from Subject `{self.name}`"
        logging.info(log_msg)

    def notify_observers(self, message: str) -> None:
        """Send a message to all observers."""
        log_msg = f"Subject `{self.name}` notifying observers: '{message}'"
        logging.info(log_msg)
        if self.observers:
            for observers in self.observers:
                observers.report_event(message, self)
        else:
            error_msg = f"Subject `{self.name}` has no observers."
            raise ObserverException(error_msg)


class Observer:
    """Observer class.

    Viewers (e.g. renderers) inherit from this class.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        log_msg = f"Observer `{self.name}` initiated"
        logging.info(log_msg)

    def report_event(self, message: str, sender: Subject) -> None:
        """Report the received message.

        Don't need to call this explicitly, it's called by Subject.dispatch().
        """
        log_msg = f"Observer `{self.name}` got message '{message}' from `{sender.name}`"
        logging.info(log_msg)
