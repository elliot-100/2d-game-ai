"""Bots can follow other Bots."""

import itertools

from logging_config import configure_logger

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleCircle
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

# Create a World
the_world = World(20, grid_size=32)

# Add a Bot to the World...
leader_a = Bot(name="A", position_from_sequence=(-5, -5))
the_world.add_entity(leader_a)

# Group of followers:
origin_a = -5, 5
for ax, ay in itertools.product(range(2), range(2)):
    position = origin_a[0] + 2 * ax, origin_a[1] + 2 * ay
    the_world.add_entity(
        Bot(
            name=f"A-{ax}{ay}",
            position_from_sequence=position,
            leader=leader_a,
            has_memory=True,
        )
    )

# Follower chain:
origin_b = 4, 7
leader_b = Bot(name="B", position_from_sequence=origin_b)
the_world.add_entity(leader_b)

for i in range(1, 4):
    bx = origin_b[0] + 0.5 * i
    by = origin_b[1] - 5 * i
    the_world.add_entity(
        Bot(
            name=f"B-{i}",
            position_from_sequence=(bx, by),
            leader=leader_b,
            has_memory=True,
        )
    )

ObstacleCircle(name="mb0", position_from_sequence=(2, -1.5), radius=2)

# Create a View of the World
view = View(world=the_world)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
