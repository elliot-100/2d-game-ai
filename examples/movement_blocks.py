"""Demonstrate implemented features using renderer."""

import logging

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.movement_block import MovementBlock
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

logging.basicConfig(level=logging.DEBUG)

# Create a World
the_world = World(
    size=300,
    grid_size=32,
)
# Add a Bot to the World...
bot = Bot(
    world=the_world,
    name="bt0",
    position_from_tuple=(-100, 0),
)
# Add a MovementBlock between Bot and destination
MovementBlock(world=the_world, name="mb0", position_from_tuple=(0, 0), radius=50)

# Create a View of the World
view = View(
    world=the_world,
    scale_factor=2,
)
MovementBlock(world=the_world, name="mb1", position_from_tuple=(100, 0), radius=20)
MovementBlock(world=the_world, name="mb3", position_from_tuple=(50, 50), radius=40)
MovementBlock(world=the_world, name="mb4", position_from_tuple=(-60, 70), radius=40)
MovementBlock(world=the_world, name="mb2", position_from_tuple=(-30, 50), radius=35)

bot.set_destination(125, 5)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
