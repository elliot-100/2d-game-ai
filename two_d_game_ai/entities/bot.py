"""Bot class."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S, Vector2
from two_d_game_ai.entities.generic_entity import _GenericEntity
from two_d_game_ai.geometry.bearing import Bearing
from two_d_game_ai.geometry.utils import point_in_or_on_circle

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class Bot(_GenericEntity):
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    destination: tuple[float, float] | None
        Destination point (World coordinates)
    destination_v: Vector2 | None
        Destination point (World coordinates)
    heading: Bearing
        Heading
    known_bots: set[Bot]
        The Bot's known but not visible peers
    name: str
    pos: tuple[float, float]
        Position (World coordinates)
    pos_v: Vector2
        Position (World coordinates)
    visible_bots: set[Bot]
        The Bot's visible peers.
    world: World

    Non-public attributes/properties
    --------------------------------
    _speed: float
        Speed as a scalar (World units / s)
        Read-only.
    _velocity_v: Vector2
        Velocity (World coordinates / s)
    """

    MAX_SPEED = 60  # World units / s
    MAX_ROTATION_RATE = 90  # degrees / s
    INITIAL_HEADING_DEGREES = 0  # degrees
    VISION_CONE_ANGLE = 90  # degrees
    DESTINATION_ARRIVAL_TOLERANCE = 1  # World units

    def __init__(self, world: World, name: str, pos: tuple[float, float]) -> None:
        super().__init__(world, name, pos)
        self._destination = tuple[float, float] | None
        self._destination_v: Vector2 | None = None
        self.heading = Bearing(Bot.INITIAL_HEADING_DEGREES)
        self.known_bots: set[Bot] = set()
        self.visible_bots: set[Bot] = set()
        self.world.bots.append(self)
        logging.info("Bot `%s` created.", self.name)

    @property
    def destination(self) -> tuple[float, float] | None:
        """Return destination."""
        if self._destination_v is not None:
            return self._destination_v.x, self._destination_v.y
        return None

    @destination.setter
    def destination(self, value: tuple[float, float]) -> None:
        self.stop()
        self._destination_v = Vector2(value)

    @property
    def destination_v(self) -> Vector2 | None:
        """Return destination vector."""
        return self._destination_v

    @destination_v.setter
    def destination_v(self, value: Vector2) -> None:
        self.stop()
        self._destination_v = value

    @property
    def _speed(self) -> float:
        """Get speed, in World units / s."""
        return self._velocity_v.magnitude()

    @property
    def is_at_destination(self) -> bool:
        """Get whether Bot is at destination (True) or not (False)."""
        if self.destination_v:
            return point_in_or_on_circle(
                self.pos_v,
                self.destination_v,
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
            self.destination_v = None
            self.stop()
            return

        if self.destination_v:
            destination_relative_bearing = self.heading.relative(
                self.destination_v - self.pos_v
            ).degrees_normalised

            #  if Bot can complete rotation to face destination this step...
            if abs(destination_relative_bearing) <= self.max_rotation_step:
                # face destination precisely
                self.rotate(-destination_relative_bearing)
                # initiate move towards destination
                self._velocity_v = self.heading.vector * Bot.MAX_SPEED

            else:
                # turn towards destination
                self.rotate(
                    math.copysign(
                        self.max_rotation_step,
                        destination_relative_bearing,
                    ),
                )
        super().update()

    def rotate(self, rotation_delta: float) -> None:
        """Change Bot rotation over 1 simulation step.

        Parameters
        ----------
        rotation_delta
            Rotation in degrees

        """
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        self.heading.vector.rotate_ip(-rotation_delta)

    def _handle_sensing(self, other_bots: list[Bot]) -> None:
        currently_visible_bots = {bot for bot in other_bots if self.can_see(bot)}
        newly_spotted_bots = currently_visible_bots - self.visible_bots
        newly_lost_bots = self.visible_bots - currently_visible_bots

        for bot in newly_spotted_bots:
            self.notify_observers(f"I've spotted `{bot.name}`")
        for bot in newly_lost_bots:
            self.notify_observers(f"I've lost sight of `{bot.name}`")

        self.visible_bots.update(newly_spotted_bots)
        self.visible_bots.difference_update(newly_lost_bots)
        self.known_bots.update(newly_lost_bots)

    def can_see(self, other_bot: Bot) -> bool:
        """Determine whether the Bot can see another Bot.

        Considers only the Bot vision cone angle.
        """
        return self.can_see_point(other_bot.pos_v)

    def can_see_point(self, point: Vector2) -> bool:
        """Determine whether the Bot can see a point.

        Considers only the Bot vision cone angle.
        """
        relative_bearing_to_point = self.heading.relative(
            point - self.pos_v
        ).degrees_normalised

        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2
