"""Demonstrate implemented features using renderer."""

import logging

from two_d_game_ai.entities import Bot
from two_d_game_ai.render.view import View
from two_d_game_ai.world import World

logging.basicConfig(level=logging.INFO)

# Create a World
the_world = World(200, 200)

# Add a Bot to the World...
b0 = Bot(
    world=the_world,
    name="b0",
    pos=(20, 20),
)

# Add another Bot to the World...
b1 = Bot(
    world=the_world,
    name="b1",
    pos=(0, 0),
)

# ... with a destination
b1.destination = (25, -50)

# Create a View of the World
view = View(
    name="the_view",
    world=the_world,
    scale_factor=2,
)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
