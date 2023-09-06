"""Define the Bot class."""

from __future__ import annotations

import math

from pygame import Vector2

from src import SIMULATION_STEP_INTERVAL_S
from src.maths import point_in_or_on_circle, relative_bearing_degrees


class Bot:
    """Simulated entity.

    Assumed circular.

    Attributes
    ----------
    destination: Vector2
        Destination
    name: str
        Name
    pos: Vector2
        Position
    heading: Vector2
        Heading
    """

    MAX_SPEED = 60  # units per simulated second
    ROTATION_RATE = 90  # degrees per simulated second
    INITIAL_HEADING = Vector2(0, 1)
    VISION_CONE_ANGLE = 90  # degrees
    DESTINATION_ARRIVAL_TOLERANCE = 1

    def __init__(self, name: str, pos: Vector2) -> None:
        self.destination: None | Vector2 = None
        self.name = name
        self.pos = pos
        self.velocity = Vector2(0, 0)
        self.heading = Bot.INITIAL_HEADING.copy()

    @property
    def speed(self) -> float:
        """Return speed."""
        return self.velocity.magnitude()

    def can_see(self, point: Vector2) -> bool:
        """Determine whether the Bot can see a point.

        Considers only the Bot vision cone angle.
        """
        relative_bearing_to_point = relative_bearing_degrees(self.heading, point)
        return abs(relative_bearing_to_point) <= Bot.VISION_CONE_ANGLE / 2

    def move(self) -> None:
        """Change Bot position over 1 simulation step."""
        self.pos += self.velocity * SIMULATION_STEP_INTERVAL_S

    def update(self) -> None:
        """Update Bot, including move over 1 simulation step."""
        if self.destination and point_in_or_on_circle(
            self.pos,
            self.destination,
            self.DESTINATION_ARRIVAL_TOLERANCE,
        ):
            self.destination = None
            self.velocity = Vector2(0)

        if self.destination:
            destination_relative_bearing = relative_bearing_degrees(
                self.heading,
                self.destination,
            )
            max_rotation_delta = self.ROTATION_RATE * SIMULATION_STEP_INTERVAL_S

            # if can complete rotation to face destination this step...
            if abs(destination_relative_bearing) <= max_rotation_delta:
                # face destination
                # self.heading.rotate_ip(destination_relative_bearing)
                # move towards destination
                self.velocity = self.heading * Bot.MAX_SPEED

            else:
                # turn towards destination
                self.heading.rotate_ip(
                    math.copysign(max_rotation_delta, destination_relative_bearing),
                )
        self.move()
