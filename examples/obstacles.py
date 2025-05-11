"""Demonstrate implemented features using renderer."""

from logging_config import configure_logger

from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.entities.obstacles import ObstacleCircle, ObstacleRectangle
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

configure_logger()

# Create a World
the_world = World(
    size=300,
    grid_size=32,
)
# Add a Bot to the World...
bot = Bot(name="bt0", position_from_sequence=(-100, 0))
the_world.add_entity(bot)

# Add an obstacle between Bot and destination
the_world.add_entity(
    ObstacleCircle(name="oc0", position_from_sequence=(0, 0), radius=50)
)

# Create a View of the World
view = View(
    world=the_world,
    scale_factor=2,
    show_debug_while_unpaused=True,
)
the_world.add_entity(
    ObstacleCircle(name="mb1", position_from_sequence=(100, 0), radius=20)
)
the_world.add_entity(
    ObstacleCircle(name="oc1", position_from_sequence=(50, 50), radius=40)
)
the_world.add_entity(
    ObstacleCircle(name="oc2", position_from_sequence=(-60, 70), radius=40)
)
the_world.add_entity(
    ObstacleCircle(name="oc3", position_from_sequence=(-30, 50), radius=35)
)

SQUARE_BLOCK_SIZE = 30, 30
the_world.add_entity(
    ObstacleRectangle(
        name="or0", position_from_sequence=(-70, -100), size=SQUARE_BLOCK_SIZE
    )
)
the_world.add_entity(
    ObstacleRectangle(
        name="or0", position_from_sequence=(-30, -100), size=SQUARE_BLOCK_SIZE
    )
)
the_world.add_entity(
    ObstacleRectangle(
        name="or0", position_from_sequence=(10, -100), size=SQUARE_BLOCK_SIZE
    )
)


bot.destination_from_sequence((125, 5))

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
