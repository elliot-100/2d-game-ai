"""Zombie demo.

Zombies chase the human if they spot them, and stop chasing if they lose sight of them.
"""

import random

from examples.logging_config import configure_logger
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

ZOMBIE_MIN_SPEED = 1
ZOMBIE_MAX_SPEED = 2
ZOMBIE_MIN_ROTATION_RATE = 5
ZOMBIE_MAX_ROTATION_RATE = 60
ZOMBIES_COUNT = 5

# Create a World
the_world = World(size_from_sequence=(20, 20))

# Add a regular human to the World
human = Bot(name="human", position_from_sequence=(0, 0))
the_world.add_generic_entity(human)

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
        vision_range=random.uniform(1, 5),
    )
    the_world.add_generic_entity(z)
    z.position = the_world.random_position()
    if set_destination:
        z.destination = the_world.random_position()
    zombies.add(z)

# Create a View of the World
view = View(world=the_world)

while view.running:
    view.handle_inputs()

    for z in zombies:
        if z.can_see(human):
            z.leader = human

    if not the_world.is_paused:
        the_world.update_()
    view.render()
