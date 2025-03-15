"""Tests for `observer_pattern` module."""

import logging

import pytest

from two_d_game_ai.entities.observer_pattern import (
    Observer,
    ObserverException,
    Subject,
)


class TestSubject:
    """Unit tests for the Subject class."""

    def test_create(self) -> None:
        """Test that a Subject is created."""
        # arrange
        # act
        s = Subject("S")
        assert s.name == "S"

    def test_notification_logged(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test notification is logged by Observer."""
        # arrange
        s = Subject("S")
        o = Observer("O")
        s.register_observer(o)
        with caplog.at_level(logging.DEBUG):
            # act
            s.notify_observers("TestDispatchMessage")
        assert "Subject 'S' notifying observers: 'TestDispatchMessage'" in caplog.text

    def test_notification_raises_exception_if_no_subscribers(self) -> None:
        """Test Exception is raised on notification if no Observers."""
        # arrange
        s = Subject("S")
        # act / assert
        with pytest.raises(ObserverException):
            s.notify_observers("TestDispatchMessage")

    def test_register_observer(self) -> None:
        """Test that an Observer is registered."""
        # arrange
        s = Subject("S")
        o = Observer("O")
        # act
        s.register_observer(o)
        assert o in s.observers

    def test_unregister_subscriber(self) -> None:
        """Test that a Subscriber is unregistered."""
        # arrange
        s = Subject("S")
        o = Observer("O")
        # act
        s.unregister_observer(o)
        assert o not in s.observers


class TestObserver:
    """Unit tests for the Observer class."""

    def test_create(self) -> None:
        """Test that Observer is created."""
        # arrange
        # act
        o = Observer("O")
        assert o.name == "O"

    def test_report_event(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test received event is logged."""
        # arrange
        s = Subject("S")
        o = Observer("O")
        s.register_observer(o)
        with caplog.at_level(logging.DEBUG):
            # act
            s.notify_observers("TestReportMessage")
        assert "Observer 'O' got 'TestReportMessage' from 'S'" in caplog.text
