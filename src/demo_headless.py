"""Demonstrate implemented features without renderer.

Should update at max 120 FPS, and report status every 1 s.
"""
from pygame import Clock

from src.demo_setup import world

MAX_SIM_FPS = 120
REPORT_INTERVAL_S = 1

clock = Clock()
loop_step = 0

while True:
    clock.tick(MAX_SIM_FPS)
    if loop_step % (MAX_SIM_FPS * REPORT_INTERVAL_S) == 0:
        print(
            f"loop time: {loop_step/MAX_SIM_FPS}  "
            f"sim elapsed: {world.step_counter/MAX_SIM_FPS}",
        )
    world.update()
    loop_step += 1
