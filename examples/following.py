"""Bots can follow other Bots."""

import itertools
import logging

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

logging.basicConfig(level=logging.INFO)


# Create a World
the_world = World(200, grid_size=32)

# Add a Bot to the World...
leader_a = Bot(name="A", position_from_sequence=(-50, -50))
the_world.add_entity(leader_a)

# Group of followers:
origin_a = -50, 50
for x, y in itertools.product(range(2), range(2)):
    position = origin_a[0] + 20 * x, origin_a[1] + 20 * y
    the_world.add_entity(
        Bot(
            name=f"A-{x}{y}",
            position_from_sequence=position,
            leader=leader_a,
        )
    )

# Follower chain:
origin_b = 40, 70
leader_b = Bot(name="B", position_from_sequence=origin_b)
the_world.add_entity(leader_b)

for i in range(1, 4):
    x = origin_b[0] + 5 * i
    y = origin_b[1] - 50 * i
    the_world.add_entity(
        Bot(name=f"B-{i}", position_from_sequence=(x, y), leader=leader_b)
    )

MovementBlock(name="mb0", position_from_sequence=(20, -15), radius=20)

# Create a View of the World
view = View(world=the_world, scale_factor=2)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
