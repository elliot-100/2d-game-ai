"""Demonstrate implemented features using renderer."""

import logging

from pygame import Vector2

from two_d_game_ai.view import View
from two_d_game_ai.world import World

logging.basicConfig(level=logging.INFO)

# Create a World
the_world = World(100)

# Add a Bot to the World...
the_world.add_bot(
    name="b0",
    pos=Vector2(20, 20),
)

# Add another Bot to the World...
the_world.add_bot(
    name="b1",
    pos=Vector2(0, 0),
)

# ... with a destination
the_world.bots["b1"].destination = Vector2(25, -50)

# Create a View of the World
view = View(
    name="the_view",
    world=the_world,
)

while view.running:
    view.handle_window_close()
    the_world.update()
    view.render()
