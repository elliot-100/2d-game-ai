"""Demonstrate implemented features using renderer."""

from pygame import Vector2

from src.view import View
from src.world import World

world = World(100)
world.add_bot(
    name="b0",
    pos=Vector2(0, 0),
)

view = View(world)

while view.running:
    view.handle_window_close()
    view.render()
