"""Tests for `Observer` class."""

import logging

import pytest

from two_d_game_ai.entities.observer import (
    Observer,
)
from two_d_game_ai.entities.subject import Subject
from two_d_game_ai.world.world import World


def test_create() -> None:
    """Test that Observer is created."""
    # arrange
    w = World(10)
    # act
    o = Observer(world=w, name="O")
    assert o.name == "O"


def test_report_event(caplog: pytest.LogCaptureFixture) -> None:
    """Test received event is logged."""
    # arrange
    w = World(10)
    s = Subject(world=w, name="S")
    o = Observer(world=w, name="O")
    s.register_observer(o)
    with caplog.at_level(logging.DEBUG):
        # act
        s.notify_observers("TestReportMessage")
    assert "Observer 'O' got 'TestReportMessage' from 'S'" in caplog.text
