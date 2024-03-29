"""Bot class."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING

from pygame import Vector2

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S
from two_d_game_ai.navigation import (
    bearing_from_vector,
    point_in_or_on_circle,
    relative_bearing_normalised,
    vector_from_bearing,
)
from two_d_game_ai.observer import Subject

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class Bot(Subject):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    destination: Vector2
        Destination point (World coordinates)
    heading: Vector2
        Heading (World coordinates)
    known_bots: set[Bot]
        The Bot's known but not visible peers
    name: str
    pos: Vector2
        Position (World coordinates)
    velocity: Vector2
        Velocity as a vector (World coordinates / s)
    visible_bots: set[Bot]
        The Bot's visible peers.
    world: World

    Read-only properties
    --------------------
    speed: float
        Speed as a scalar (World units / s)
    """

    MAX_SPEED = 60  # World units / s
    MAX_ROTATION_RATE = 90  # degrees / s
    INITIAL_HEADING_DEGREES = 0  # degrees
    VISION_CONE_ANGLE = 90  # degrees
    DESTINATION_ARRIVAL_TOLERANCE = 1  # World units

    def __init__(self, world: World, name: str, pos: Vector2) -> None:
        super().__init__(name)
        self.world = world
        self.destination: None | Vector2 = None
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.heading = vector_from_bearing(Bot.INITIAL_HEADING_DEGREES)
        self.visible_bots: set[Bot] = set()
        self.known_bots: set[Bot] = set()
        self.world.bots.append(self)
        logging.info("Bot `%s` created.", self.name)

    @property
    def speed(self) -> float:
        """Return speed."""
        return self.velocity.magnitude()

    @property
    def heading_degrees(self) -> float:
        """Return heading in degrees."""
        return bearing_from_vector(self.heading)

    @property
    def is_at_destination(self) -> bool:
        """Return True if at destination."""
        if self.destination:
            return point_in_or_on_circle(
                self.pos,
                self.destination,
                self.DESTINATION_ARRIVAL_TOLERANCE,
            )
        return False

    @property
    def max_rotation_delta(self) -> float:
        """Return maximum rotation in one simulation step."""
        return self.MAX_ROTATION_RATE * SIMULATION_STEP_INTERVAL_S

    def move(self) -> None:
        """Change Bot position over 1 simulation step."""
        self.pos += self.velocity * SIMULATION_STEP_INTERVAL_S

    def update(self, other_bots: list[Bot]) -> None:
        """Update Bot, including move over 1 simulation step."""
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

        if self.is_at_destination:
            self.notify_observers("I've reached destination")
            self.destination = None
            self.velocity = Vector2(0)
            return

        if self.destination:
            destination_relative_bearing = relative_bearing_normalised(
                self.heading,
                self.destination - self.pos,
            )

            #  if Bot can complete rotation to face destination this step...
            if self.max_rotation_delta >= abs(destination_relative_bearing):
                # face destination precisely
                # NB legacy use of Pygame CCW rotation here:
                self.heading.rotate_ip(-destination_relative_bearing)
                # move towards destination
                self.velocity = self.heading * Bot.MAX_SPEED

            else:
                # turn towards destination
                self.heading.rotate_ip(
                    math.copysign(
                        self.max_rotation_delta,
                        # NB legacy use of Pygame CCW rotation here:
                        -destination_relative_bearing,
                    ),
                )
        self.move()

    def can_see(self, other_bot: Bot) -> bool:
        """Determine whether the Bot can see another Bot.

        Considers only the Bot vision cone angle.
        """
        return self.can_see_point(other_bot.pos)

    def can_see_point(self, point: Vector2) -> bool:
        """Determine whether the Bot can see a point.

        Considers only the Bot vision cone angle.
        """
        relative_bearing_to_point = relative_bearing_normalised(self.heading, point)
        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2
