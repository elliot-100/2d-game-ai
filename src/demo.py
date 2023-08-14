"""Demonstrate implemented features using renderer."""

from src.demo_setup import world
from src.view import View

# Create a View of the World
view = View(world)

while view.running:
    view.handle_window_close()
    world.update()
    view.render()
