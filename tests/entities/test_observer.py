"""Test the Observer pattern."""

import logging

import pytest

from two_d_game_ai.entities.observer_pattern import (
    ObserverException,
    _Observer,
    _Subject,
)


class TestSubject:
    """Unit tests for the Subject class."""

    def test_create(self) -> None:
        """Test that a Subject is created."""
        s = _Subject("S")
        assert s.name == "S"

    def test_notification_logged(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test notification is logged by Observer."""
        caplog.set_level(logging.INFO)
        s = _Subject("S")
        o = _Observer("O")
        s.register_observer(o)

        s.notify_observers("TestDispatchMessage")
        assert (
            "root",
            logging.INFO,
            "Subject `S` notifying observers: 'TestDispatchMessage'",
        ) in caplog.record_tuples

    def test_notification_raises_exception_if_no_subscribers(self) -> None:
        """Test Exception is raised on notification if no Observers."""
        s = _Subject("S")

        with pytest.raises(ObserverException):
            s.notify_observers("TestDispatchMessage")

    def test_register_observer(self) -> None:
        """Test that an Observer is registered."""
        s = _Subject("S")
        o = _Observer("O")

        s.register_observer(o)
        assert o in s.observers

    def test_unregister_subscriber(self) -> None:
        """Test that a Subscriber is unregistered."""
        s = _Subject("S")
        o = _Observer("O")

        s.unregister_observer(o)
        assert o not in s.observers


class TestObserver:
    """Unit tests for the Observer class."""

    def test_create(self) -> None:
        """Test that Observer is created."""
        o = _Observer("O")
        assert o.name == "O"

    def test_report_event(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test received event is logged."""
        caplog.set_level(logging.INFO)
        s = _Subject("S")
        o = _Observer("O")
        s.register_observer(o)

        s.notify_observers("TestReportMessage")
        assert (
            "root",
            logging.INFO,
            "Observer `O` got message 'TestReportMessage' from `S`",
        ) in caplog.record_tuples
