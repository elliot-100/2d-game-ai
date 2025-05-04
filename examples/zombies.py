"""Zombie demo.

Zombies chase the human if they spot them, and stop chasing if they lose sight of them.
"""

import logging
import random

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

logging.basicConfig(level=logging.DEBUG)

ZOMBIE_MIN_SPEED = 1
ZOMBIE_MAX_SPEED = 8
ZOMBIE_MIN_ROTATION_RATE = 5
ZOMBIE_MAX_ROTATION_RATE = 60
ZOMBIES_COUNT = 5


# Create a World
the_world = World(100)

# Add a regular human to the World
human = Bot(name="human", max_speed=10, position_from_sequence=(0, 0))
the_world.add_entity(human)

# Add zombies with varying speeds and vision ranges, and set destination for some
zombies = set()
for i in range(ZOMBIES_COUNT):
    set_destination = i < ZOMBIES_COUNT / 4
    z = Bot(
        name=f"z{i}",
        max_speed=random.uniform(ZOMBIE_MIN_SPEED, ZOMBIE_MAX_SPEED),
        max_rotation_rate=random.uniform(
            ZOMBIE_MIN_ROTATION_RATE, ZOMBIE_MAX_ROTATION_RATE
        ),
        position_from_sequence=(0, 0),
        initial_heading=random.uniform(0, 360),
        vision_range=random.uniform(10, 50),
    )
    the_world.add_entity(z)
    z.position = the_world.random_location()
    if set_destination:
        z.destination = the_world.random_location()
    zombies.add(z)

# Create a View of the World
view = View(world=the_world, scale_factor=4)

while view.running:
    view.handle_inputs()

    for z in zombies:
        if z.can_see(human):
            z.leader = human

    if not the_world.is_paused:
        the_world.update()
    view.render()
