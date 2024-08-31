"""Demonstrate implemented features using renderer."""

import logging

from two_d_game_ai.entities import Bot, MovementBlock
from two_d_game_ai.render.view import View
from two_d_game_ai.world import World

logging.basicConfig(level=logging.INFO)

# Create a World
the_world = World(300)

# Add a Bot to the World...
bot = Bot(
    world=the_world,
    name="bt0",
    pos=(-100, 0),
)

# ... with a destination
bot.destination = (100, -0)

# Add a MovementBlock between Bot and destination
movement_block = MovementBlock(
    world=the_world, name="mb0", pos=(0, 0), collision_radius=50
)

# Create a View of the World
view = View(
    name="the_view",
    world=the_world,
    scale_factor=1,
    margin=40,
)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
