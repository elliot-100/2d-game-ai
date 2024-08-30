"""Package containing `Bot` class."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING, ClassVar

from two_d_game_ai import SIMULATION_STEP_INTERVAL_S, Vector2
from two_d_game_ai.entities.generic_entity import GenericEntity
from two_d_game_ai.geometry import point_in_or_on_circle
from two_d_game_ai.geometry.bearing import Bearing

if TYPE_CHECKING:
    from two_d_game_ai.world import World


class Bot(GenericEntity):
    """Simulated entity.

    Assumed circular.

    Non-public attributes/properties
    --------------------------------
    _speed
        Speed as a scalar (World units / s)
        Read-only.
    _velocity_v
        Velocity (World coordinates / s)
    """

    MAX_SPEED: ClassVar[float] = 60
    """World units / second."""
    MAX_ROTATION_RATE: ClassVar[float] = 90
    """Degrees / second."""
    INITIAL_HEADING_DEGREES: ClassVar[float] = 0
    VISION_CONE_ANGLE: ClassVar[float] = 90
    """Degrees."""
    _DESTINATION_ARRIVAL_TOLERANCE: ClassVar[float] = 1
    """World units."""

    def __init__(self, world: World, name: str, pos: tuple[float, float]) -> None:
        super().__init__(world, name, pos)
        self._velocity_v = Vector2(0, 0)
        self._destination_v: Vector2 | None = None
        self.heading: Bearing = Bearing(Bot.INITIAL_HEADING_DEGREES)
        self.known_bots: set[Bot] = set()
        """Peers which are known about, but aren't currently in sight."""
        self.visible_bots: set[Bot] = set()
        """Peers which are currently in sight."""
        self.world.bots.append(self)
        logging.info("Bot `%s` created.", self.name)

    @property
    def destination(self) -> tuple[float, float] | None:
        """Destination point in World coordinates."""
        if self._destination_v is not None:
            return self._destination_v.x, self._destination_v.y
        return None

    @destination.setter
    def destination(self, value: tuple[float, float]) -> None:
        self.stop()
        self.destination_v = Vector2(value)

    @property
    def destination_v(self) -> Vector2 | None:
        """Destination point in World coordinates, as `Vector2`."""
        return self._destination_v

    @destination_v.setter
    def destination_v(self, value: Vector2) -> None:
        if value is None or self.world.point_is_inside_world_bounds(value):
            self.stop()
            self._destination_v = value

    @property
    def is_at_destination(self) -> bool:
        """Get whether Bot is at destination (True) or not (False)."""
        if self.destination_v:
            return point_in_or_on_circle(
                self.pos_v,
                self.destination_v,
                self._DESTINATION_ARRIVAL_TOLERANCE,
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
        self._move()

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
        self._velocity_v = Vector2(0)

    def _move(self) -> None:
        """Change position over 1 simulation step."""
        self.pos_v += self._velocity_v * SIMULATION_STEP_INTERVAL_S

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

    def route_to(
        self,
        goal: Vector2 | None,
    ) -> list[Vector2]:
        """Perform uniform cost search for `goal`.

        Variation of Dijkstra's algorithm.

        Returns
        -------
        list[GridRef]
            Locations on the path to `goal`.
            Empty if no path found.
        """
        # Early return case:
        if goal is None:
            return []

        grid = self.world.grid
        goal_cell = GridRef.cell_from_pos(self.world, goal)
        start_cell = GridRef.cell_from_pos(self.world, self.pos_v)

        # More early return cases:
        if (
            goal_cell in grid.untraversable_cells
            or start_cell in grid.untraversable_cells
            or goal_cell == start_cell
        ):
            return []

        came_from: dict[GridRef, GridRef | None] = {start_cell: None}
        cost_so_far: dict[GridRef, float] = {start_cell: 0}
        frontier: PriorityQueue = PriorityQueue()
        frontier.put(0, start_cell)

        while not frontier.is_empty:
            current_location = frontier.get()

            if current_location == goal_cell:  # early exit
                break

            for new_location in grid.reachable_neighbours(current_location):
                new_cost = cost_so_far[current_location] + grid.cost(
                    current_location, new_location
                )
                if (
                    new_location not in came_from
                    or new_cost < cost_so_far[new_location]
                    # add new_location to frontier if cheaper
                ):
                    cost_so_far[new_location] = new_cost
                    frontier.put(priority=new_cost, location=new_location)
                    came_from[new_location] = current_location

        # Construct path starting at goal and retracing to agent location...
        path_from_goal = [goal_cell.cell_centre_to_pos(self.world)]
        current_location = goal_cell

        while current_location is not start_cell:
            came_from_location = came_from.get(current_location)
            if came_from_location is None:
                return []
            current_location = came_from_location
            path_from_goal.append(current_location.cell_centre_to_pos(self.world))

        del path_from_goal[-1]  # don't include start cell
        path_from_goal[0] = goal  # use precise destination for last waypoint

        return list(reversed(path_from_goal))
