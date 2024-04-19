"""Bot class."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.bearing import Bearing
from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.navigation import (
    point_in_or_on_circle,
)

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class Bot(GenericEntity):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    destination: Vector2
        Destination point (World coordinates)
    heading: Bearing
        Heading
    known_bots: set[Bot]
        The Bot's known but not visible peers
    name: str
    pos: Vector2
        Position (World coordinates)
    visible_bots: set[Bot]
        The Bot's visible peers.
    world: World

    Non-public attributes/properties
    --------------------------------
    _speed: float
        Speed as a scalar (World units / s)
        Read-only.
    _velocity: Vector2
        Velocity as a vector (World coordinates / s)

    """

    MAX_SPEED = 60  # World units / s
    MAX_ROTATION_RATE = 90  # degrees / s
    INITIAL_HEADING_DEGREES = 0  # degrees
    VISION_CONE_ANGLE = 90  # degrees
    DESTINATION_ARRIVAL_TOLERANCE = 1  # World units

    def __init__(self, world: World, name: str, pos: Vector2) -> None:
        super().__init__(world, name, pos)
        self.destination: None | Vector2 = None
        self.heading = Bearing(Bot.INITIAL_HEADING_DEGREES)
        self.known_bots: set[Bot] = set()
        self.visible_bots: set[Bot] = set()
        self._velocity = Vector2(0, 0)

        self.world.bots.append(self)
        logging.info("Bot `%s` created.", self.name)

    @property
    def _speed(self) -> float:
        """Get speed, in World units / s."""
        return self._velocity.magnitude()

    @property
    def is_at_destination(self) -> bool:
        """Get whether Bot is at destination (True) or not (False)."""
        if self.destination:
            return point_in_or_on_circle(
                self.pos,
                self.destination,
                self.DESTINATION_ARRIVAL_TOLERANCE,
            )
        return False

    @property
    def max_rotation_step(self) -> float:
        """Get maximum rotation, in degrees per simulation step."""
        return self.MAX_ROTATION_RATE * SIMULATION_STEP_INTERVAL_S

    def update(self, other_bots: list[Bot]) -> None:
        """Update Bot, including move over 1 simulation step."""
        self._handle_sensing(other_bots)

        if self.is_at_destination:
            self.notify_observers("I've reached destination")
            self.destination = None
            self._velocity = Vector2(0)
            return

        if self.destination:
            destination_relative_bearing = self.heading.relative(
                self.destination - self.pos
            ).degrees_normalised

            #  if Bot can complete rotation to face destination this step...
            if abs(destination_relative_bearing) <= self.max_rotation_step:
                # face destination precisely
                self.rotate(-destination_relative_bearing)
                # initiate move towards destination
                self._velocity = self.heading.vector * Bot.MAX_SPEED

            else:
                # turn towards destination
                self.rotate(
                    math.copysign(
                        self.max_rotation_step,
                        destination_relative_bearing,
                    ),
                )
        self.move()

    def rotate(self, rotation_delta: float) -> None:
        """Change Bot rotation over 1 simulation step.

        Parameters
        ----------
        rotation_delta
            Rotation in degrees

        """
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        self.heading.vector.rotate_ip(-rotation_delta)

    def move(self) -> None:
        """Change Bot position over 1 simulation step."""
        self.pos += self._velocity * SIMULATION_STEP_INTERVAL_S

    def _handle_sensing(self, other_bots: list[Bot]) -> None:
        currently_visible_bots = {bot for bot in other_bots if self.can_see(bot)}
        newly_spotted_bots = currently_visible_bots - self.visible_bots
        newly_lost_bots = self.visible_bots - currently_visible_bots

        if newly_spotted_bots:
            for newly_spotted_bot in newly_spotted_bots:
                self.notify_observers(f"I've spotted `{newly_spotted_bot.name}`")
                self.visible_bots.add(newly_spotted_bot)
        if newly_lost_bots:
            for newly_lost_bot in newly_lost_bots:
                self.notify_observers(f"I've lost sight of `{newly_lost_bot.name}`")
                self.visible_bots.remove(newly_lost_bot)
                self.known_bots.add(newly_lost_bot)

    def can_see(self, other_bot: Bot) -> bool:
        """Determine whether the Bot can see another Bot.

        Considers only the Bot vision cone angle.
        """
        return self.can_see_point(other_bot.pos)

    def can_see_point(self, point: Vector2) -> bool:
        """Determine whether the Bot can see a point.

        Considers only the Bot vision cone angle.
        """
        relative_bearing_to_point = self.heading.relative(
            point - self.pos
        ).degrees_normalised

        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2
