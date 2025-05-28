"""TO DO."""

from examples.logging_config import configure_logger
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleRectangle
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

# Create a World
the_world = World(
    size=32,
    grid_size=8,
)
GRID_CELL_SIZE = 4, 4

# Add a Bot to the World...
bot = Bot(name="bt0", position_from_sequence=(0, 0))
the_world.add_entity(bot)


# Create a View of the World
view = View(
    world=the_world,
    show_debug_while_unpaused=True,
)


the_world.add_entity(
    ObstacleRectangle(name="or0", position_from_sequence=(4, 4), size=GRID_CELL_SIZE)
)

the_world.add_entity(
    ObstacleRectangle(name="or0", position_from_sequence=(4, -4), size=GRID_CELL_SIZE)
)

bot.destination_from_sequence((12, 12))

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
