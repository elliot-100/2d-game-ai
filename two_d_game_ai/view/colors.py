"""Contains colour definitions."""

from pygame import Color

DEBUG = Color("magenta")

WINDOW_FILL = Color("grey15")
WINDOW_TEXT = Color("grey80")

WORLD_FILL = Color("grey25")
WORLD_AXES_LINE = WORLD_GRID_LINE = Color("grey40")

MOVEMENT_BLOCK_FILL = Color("aqua")
MOVEMENT_BLOCK_LINE = DEBUG
VISION_BLOCK_FILL = Color("palevioletred")  # smoke-like
VISION_BLOCK_LINE = DEBUG
MOVEMENT_AND_VISION_BLOCK_FILL = Color("grey40")  # glass-like
MOVEMENT_AND_VISION_BLOCK_LINE = DEBUG

BOT_FILL = Color("white")
BOT_HEADING_INDICATOR_LINE = WINDOW_FILL
BOT_DESTINATION_LINE = Color("white")
BOT_ROUTE_LINE = Color("orange")
BOT_CAN_SEE_LINE = Color("green2")
BOT_KNOWS_LINE = Color("dodgerblue")

SELECTED_FILL = Color("yellow")
