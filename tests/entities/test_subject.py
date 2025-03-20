"""Tests for `Subject` class."""

import logging

import pytest

from two_d_game_ai.entities.observer import (
    Observer,
    ObserverException,
)
from two_d_game_ai.entities.subject import Subject
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that a Subject is created."""
    # arrange
    w = World(10)
    # act
    s = Subject(world=w, name="S")
    assert s.name == "S"


def test_register_observer() -> None:
    """Test that an Observer is registered."""
    # arrange
    w = World(10)
    s = Subject(world=w, name="S")
    o = Observer(world=w, name="O")
    # act
    s.register_observer(o)
    assert o in s.observers


def test_notification_logged(caplog: pytest.LogCaptureFixture) -> None:
    """Test notification is logged by Observer."""
    # arrange
    w = World(10)
    s = Subject(world=w, name="S")
    o = Observer(world=w, name="O")
    s.register_observer(o)
    with caplog.at_level(logging.DEBUG):
        # act
        s.notify_observers("TestDispatchMessage")
    assert "Subject 'S' notifying observers: 'TestDispatchMessage'" in caplog.text


def test_notification_raises_exception_if_no_subscribers() -> None:
    """Test Exception is raised on notification if no Observers."""
    # arrange
    w = World(10)
    s = Subject(world=w, name="S")
    # act / assert
    with pytest.raises(ObserverException):
        s.notify_observers("TestDispatchMessage")


def test_unregister_observer() -> None:
    """Test that an Observer is unregistered."""
    # arrange
    w = World(10)
    s = Subject(world=w, name="S")
    o = Observer(world=w, name="O")
    # act
    s.unregister_observer(o)
    assert o not in s.observers
