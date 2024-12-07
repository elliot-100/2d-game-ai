"""
# Architecture

The `World` (`two_d_game_ai.world.world.World`) is the simulated domain.
- `World.grid` refers to a `Grid` (`two_d_game_ai.world.grid.Grid`), used for
  pathfinding and line-of-sight.

`Bot`s are simulated agents/vehicles.
- They are aware of the `World`.
- They are not aware of the `World.grid`, but it does constrain their behaviour, e.g.
  when they query the `World` to find a route to a destination, intermediate waypoints
  on the path are on grid nodes (cell centres).


`View` (`two_d_game_ai.view.view.View`) provides a visual user interface.

"""

SIMULATION_FPS: int = 60
"""Simulation frames per second.
Views could update faster or slower."""
