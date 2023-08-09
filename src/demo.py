"""Demonstrate implemented features using renderer."""

from pygame import Vector2

from src.view import View
from src.world import World

# Create a World
world = World(100)

# Add a Bot to the World...
world.add_bot(
    name="b0",
    pos=Vector2(0, 0),
)

# ... with a velocity vector
world.bots["b0"].velocity = Vector2(1, 0)

# Add another Bot to the World...
world.add_bot(
    name="b1",
    pos=Vector2(0, 0),
)

# ... with a destination
world.bots["b1"].destination = Vector2(-25, 50)


# Create a View of the World
view = View(world)

while view.running:
    view.handle_window_close()
    world.update()
    view.render()
