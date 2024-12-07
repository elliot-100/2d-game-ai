"""Module containing `PriorityQueue` class."""

import heapq
from dataclasses import dataclass
from typing import Self

from two_d_game_ai.world.grid_ref import GridRef


class PriorityQueue:
    """Simple priority queue, using heapq.

    Specialised for holding locations.
    """

    def __init__(self) -> None:
        self.items: list[PrioritisedLocation] = []

    @property
    def is_empty(self) -> bool:
        """Check whether the queue is empty."""
        return not self.items

    def put(self, priority: float, location: GridRef) -> None:
        """Add a location with priority."""
        heapq.heappush(self.items, PrioritisedLocation(priority, location))

    def get(self) -> GridRef:
        """Remove and return the highest priority location.

        NB this is the lowest `priority` value.
        """
        return heapq.heappop(self.items).location


@dataclass
class PrioritisedLocation:
    """Wrapper for prioritised location.

    Avoids unintended prioritisation attempts on `location` itself.
    """

    priority: float
    location: GridRef

    def __lt__(self, other: Self) -> bool:
        """Determine priority for `heapq`."""
        return self.priority < other.priority
