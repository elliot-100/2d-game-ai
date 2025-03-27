"""Contains `Bot` class."""

from __future__ import annotations

import logging
import math
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, ClassVar

from pygame import Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import Bearing, point_in_or_on_circle

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Bot(GenericEntity):
    """Simulated agent/vehicle."""

    DEFAULT_MAX_SPEED: ClassVar[float] = 6
    """`World` units / second."""
    DEFAULT_MAX_ROTATION_RATE: ClassVar[float] = 90
    """Degrees / second."""
    DEFAULT_INITIAL_HEADING: ClassVar[float] = 0
    """Degrees."""
    VISION_CONE_ANGLE: ClassVar[float] = 90
    """Degrees."""
    DEFAULT_VISION_RANGE: ClassVar[float] = 100
    """`World` units."""
    POSITION_ARRIVAL_TOLERANCE: ClassVar[float] = 1
    """`World` units."""

    leader: Bot | None = None
    max_speed: float = DEFAULT_MAX_SPEED
    """`World` units / second."""
    max_rotation_rate: float = DEFAULT_MAX_ROTATION_RATE
    """Degrees / second."""
    initial_heading: InitVar[float] = DEFAULT_INITIAL_HEADING
    """Initial direction the `Bot` is facing. Degrees."""
    has_memory: bool = False
    """Can remember peers."""
    vision_range: float = DEFAULT_VISION_RANGE
    """`World` units."""

    heading: Bearing = field(init=False)
    """Direction the `Bot` is facing."""
    velocity: Vector2 = field(init=False)
    route: list[Vector2] = field(init=False, default_factory=list)
    """Waypoints to be visited, in order."""
    visible_bots: set[Bot] = field(init=False, default_factory=set)
    """Peers which are currently in sight."""
    remembered_bots: set[Bot] = field(init=False, default_factory=set)
    """Peers which are known about, but aren't currently in sight."""

    _destination: Vector2 | None = field(init=False, default=None)

    def __post_init__(
        self, position_from_sequence: Sequence[float], initial_heading: float
    ) -> None:
        super().__post_init__(position_from_sequence)
        self.heading: Bearing = Bearing(initial_heading)
        self.velocity: Vector2 = Vector2(0, 0)
        self.destination = None
        log_msg = f"Bot '{self.name}' initialised."
        logger.info(log_msg)

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def max_rotation_step(self) -> float:
        """Get maximum rotation, in degrees per simulation step."""
        return self.max_rotation_rate / SIMULATION_FPS

    @property
    def destination(self) -> Vector2 | None:
        """Destination point in `World` coordinates."""
        return self._destination

    @destination.setter
    def destination(self, proposed_destination: Vector2 | None) -> None:
        """Set destination point."""
        if proposed_destination is None:
            log_msg = f"Bot '{self.name}': destination -> `None`."
            logger.debug(log_msg)
            self._destination = None
            return

        if (
            proposed_destination != self.position
            and not self.is_at(proposed_destination)
            and self.world.location_is_inside_world_bounds(proposed_destination)
        ):
            log_msg = f"Bot '{self.name}': destination -> `{proposed_destination}`."
            logger.info(log_msg)
            self.stop()
            self._destination = proposed_destination
            self.route = self.route_to(self.destination)
            log_msg = f"Bot '{self.name}': routed: {len(self.route)} waypoints."
            logger.info(log_msg)
            if self.route and len(self.route) >= 2:  # noqa: PLR2004
                del self.route[0]
                # effectively suppress reporting arrival at first waypoint, which is
                # always own position

    def destination_from_sequence(self, position: Sequence[float]) -> None:
        """Set destination point."""
        self.destination = Vector2(position)

    def update(self) -> None:
        """Update `Bot`, including move over 1 simulation step."""
        self.handle_sensing(b for b in self.world.bots if b is not self)

        if self.leader and self.destination != self.leader.position:
            self.destination = self.leader.position.copy()

        if self.route:
            if self.destination is None:
                raise TypeError
            if self.is_at(self.destination):
                log_msg = f"Bot '{self.name}': arrived at destination."
                logger.info(log_msg)
                self.stop()
                self.route = []
                self.destination = None
                return

            if self.is_at(self.route[0]):
                log_msg = f"Bot '{self.name}': arrived at waypoint."
                logger.info(log_msg)
                self.stop()
                del self.route[0]
                return

            waypoint_relative_bearing = self.heading.relative(
                self.route[0] - self.position
            ).degrees_normalised

            #  if Bot can complete rotation to face wp this step...
            if abs(waypoint_relative_bearing) <= self.max_rotation_step:
                # face wp precisely
                self.rotate(waypoint_relative_bearing)
                # initiate move towards wp
                self.velocity = self.heading.vector * self.max_speed

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
        """Get whether `Bot` is at location (True) or not (False)."""
        return point_in_or_on_circle(
            self.position,
            location,
            self.POSITION_ARRIVAL_TOLERANCE,
        )

    def rotate(self, rotation_delta: float) -> None:
        """Change `Bot` rotation over 1 simulation step.

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
        """Change `Bot` position over 1 simulation step."""
        self.position += self.velocity / SIMULATION_FPS

    def handle_sensing(self, other_bots: Iterable[Bot]) -> None:
        """Update knowledge of others."""
        currently_visible_bots = {bot for bot in other_bots if self.can_see(bot)}
        newly_lost_bots = self.visible_bots - currently_visible_bots

        if self.has_memory:
            self.remembered_bots.update(newly_lost_bots)
        elif self.leader not in currently_visible_bots:
            self.leader = None

        self.visible_bots = currently_visible_bots

    def can_see(self, other_bot: Bot) -> bool:
        """Determine whether `Bot` can see another `Bot`.

        Considers only vision cone angle.
        """
        return self.can_see_location(other_bot.position)

    def can_see_location(self, location: Vector2) -> bool:
        """Determine whether `Bot` can see `location`.

        Considers only vision cone angle.
        """
        relative_vector = location - self.position
        relative_bearing_magnitude = abs(
            self.heading.relative(relative_vector).degrees_normalised
        )

        return (
            relative_bearing_magnitude <= Bot.VISION_CONE_ANGLE / 2
            and relative_vector.magnitude() < self.vision_range
        )

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
        return [] if goal is None else self.world.route(self.position, goal)
