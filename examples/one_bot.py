"""Demo a single Bot."""

from logging_config import configure_logger

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

# Create a World
the_world = World(400)

# Add a Bot to the World...
the_world.add_entity(Bot(position_from_sequence=(20, 20)))

# Create a View of the World
view = View(
    world=the_world,
    scale_factor=0.7,
)

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
