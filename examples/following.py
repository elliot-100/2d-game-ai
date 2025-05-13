"""Bots can follow other Bots."""

import itertools

from examples.logging_config import configure_logger
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleRectangle
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

# Create a World
the_world = World(40, grid_size=16)

# Add a Bot to the World...
leader_a = Bot(name="A", position_from_sequence=(-10, -10))
the_world.add_entity(leader_a)

# Group of followers:
origin = -10, 10
offset = 2, 2
for i in range(4):
    pos = origin[0] + offset[0] * i, origin[1] + offset[1] * i
    the_world.add_entity(
        Bot(
            name=f"A{i}",
            position_from_sequence=pos,
            leader=leader_a,
            has_memory=True,
        )
    )

# Follower chain:
origin = 10, -10
offset = 2, 2
leader_b = Bot(name="B", position_from_sequence=origin)
the_world.add_entity(leader_b)

for i in range(1, 4):
    pos = origin[0] + offset[0] * i, origin[1] + offset[1] * i
    the_world.add_entity(
        Bot(
            name=f"B{i}",
            position_from_sequence=pos,
            leader=leader_b,
            has_memory=True,
        )
    )

the_world.add_entity(
    ObstacleRectangle(name="mb0", position_from_sequence=(-14, 0), size=(10, 2))
)
the_world.add_entity(
    ObstacleRectangle(name="mb1", position_from_sequence=(2, 0), size=(10, 2))
)

# Create a View of the World
view = View(world=the_world, show_debug_while_unpaused=True)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
