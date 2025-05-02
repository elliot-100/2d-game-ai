"""Demonstrate implemented features using renderer."""

import logging

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

logging.basicConfig(level=logging.INFO)

# Create a World
the_world = World(200)

# Add a Bot to the World...
the_world.add_entity(Bot(name="b0", position_from_sequence=(20, 20)))
# Create a View of the World
view = View(
    world=the_world,
    scale_factor=2,
)
# Add another Bot to the World...
b1 = Bot(name="b1", position_from_sequence=(0, 0))
the_world.add_entity(b1)
# ... with a destination
b1.destination_from_sequence((25, -50))

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
