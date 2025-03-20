"""Demonstrate implemented features using renderer."""

import logging

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

logging.basicConfig(level=logging.DEBUG)

# Create a World
the_world = World(200)

# Add a Bot to the World...
b0 = Bot(
    world=the_world,
    name="b0",
    position_from_tuple=(20, 20),
)
# Create a View of the World
view = View(
    world=the_world,
    scale_factor=2,
)
# Add another Bot to the World...
b1 = Bot(
    world=the_world,
    name="b1",
    position_from_tuple=(0, 0),
)
# ... with a destination
b1.set_destination(25, -50)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
