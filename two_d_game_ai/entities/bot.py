"""Package containing `Bot` class."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import ClassVar

from pygame import Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.entities.observer_pattern import Subject
from two_d_game_ai.geometry import Bearing, point_in_or_on_circle

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Bot(GenericEntity):
    """Simulated agent/vehicle."""

    MAX_SPEED: ClassVar[float] = 60
    """World units / second."""
    MAX_ROTATION_RATE: ClassVar[float] = 90
    """Degrees / second."""
    INITIAL_HEADING_DEGREES: ClassVar[float] = 0
    VISION_CONE_ANGLE: ClassVar[float] = 90
    """Degrees."""
    POSITION_ARRIVAL_TOLERANCE: ClassVar[float] = 1
    """World units."""

    heading: Bearing = field(init=False)
    """Direction the `Bot` is facing."""
    velocity: Vector2 = field(init=False)
    route: list[Vector2] = field(default_factory=list)
    """Waypoints to be visited."""
    known_bots: set[Bot] = field(default_factory=set)
    """Peers which are known about, but aren't currently in sight."""
    visible_bots: set[Bot] = field(default_factory=set)
    """Peers which are currently in sight."""

    _destination: Vector2 | None = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self.heading: Bearing = Bearing(self.INITIAL_HEADING_DEGREES)
        self.velocity: Vector2 = Vector2(0, 0)
        self.world.bots.add(self)
        log_msg = f"Bot '{self.name}' created."
        logger.info(log_msg)

    def __hash__(self) -> int:
        return Subject.__hash__(self)

    @property
    def destination(self) -> Vector2 | None:
        """Destination point in World coordinates."""
        return self._destination

    @destination.setter
    def destination(self, value: Vector2 | None) -> None:
        """Set destination point."""
        if value is None:
            self._destination = None
        elif self.world.point_is_inside_world_bounds(value):
            self.stop()
            self._destination = value
            self.route = self.route_to(self._destination)
            log_msg = f"Bot '{self.name}' destination set: {self._destination}."
            logger.info(log_msg)
            log_msg = (
                f"Bot '{self.name}' route calculated: {len(self.route)} waypoints."
            )
            logger.info(log_msg)

    def set_destination(self, *args: float) -> None:
        """Set destination point as pair of floats, avoiding `Vector2`.

        For use in example scripts.
        """
        self.destination = Vector2(args[0], args[1])

    @property
    def max_rotation_step(self) -> float:
        """Get maximum rotation, in degrees per simulation step."""
        return self.MAX_ROTATION_RATE / SIMULATION_FPS

    def update(self, other_bots: set[Bot]) -> None:
        """Update Bot, including move over 1 simulation step."""
        self._handle_sensing(other_bots)

        if self.route and self.is_at(self.route[0]):
            self.notify_observers("I've reached next waypoint.")
            del self.route[0]
            self.stop()

        if self.destination and self.is_at(self.destination):
            self.notify_observers("I've reached destination.")
            self.destination = None
            self.stop()
            return

        if self.route:
            waypoint_relative_bearing = self.heading.relative(
                self.route[0] - self.pos
            ).degrees_normalised

            #  if Bot can complete rotation to face wp this step...
            if abs(waypoint_relative_bearing) <= self.max_rotation_step:
                # face wp precisely
                self.rotate(-waypoint_relative_bearing)
                # initiate move towards wp
                self.velocity = self.heading.vector * Bot.MAX_SPEED

            else:
                # turn towards wp
                self.rotate(
                    math.copysign(
                        self.max_rotation_step,
                        waypoint_relative_bearing,
                    ),
                )
        self._move()

    def is_at(self, location: Vector2) -> bool:
        """Get whether Bot is at location (True) or not (False)."""
        return point_in_or_on_circle(
            self.pos,
            location,
            self.POSITION_ARRIVAL_TOLERANCE,
        )

    def rotate(self, rotation_delta: float) -> None:
        """Change Bot rotation over 1 simulation step.

        Parameters
        ----------
        rotation_delta
            Rotation in degrees

        """
        # NB legacy use of Pygame CCW rotation here, thus negative angle:
        self.heading.vector.rotate_ip(-rotation_delta)

    def stop(self) -> None:
        """Stop."""
        self.velocity = Vector2(0)

    def _move(self) -> None:
        """Change position over 1 simulation step."""
        self.pos += self.velocity / SIMULATION_FPS

    def _handle_sensing(self, other_bots: set[Bot]) -> None:
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
        return self.can_see_point(other_bot.pos)

    def can_see_point(self, point: Vector2) -> bool:
        """Determine whether the Bot can see a point.

        Considers only the Bot vision cone angle.
        """
        relative_bearing_to_point = self.heading.relative(
            point - self.pos
        ).degrees_normalised

        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2

    def route_to(
        self,
        goal: Vector2 | None,
    ) -> list[Vector2]:
        """Determine route to `goal`.

        Returns
        -------
        list[Vector2]
            Locations on the path to `goal`, including `goal` itself.
            Empty if no path found.
        """
        return [] if goal is None else self.world.route(self.pos, goal)
