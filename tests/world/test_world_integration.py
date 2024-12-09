"""Test integration of `World` and other classes."""

from pygame import Vector2

from two_d_game_ai import SIMULATION_FPS
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.world.world import World


def test_bot_move_in_world_context() -> None:
    """Test that Bot's position is correct after 1 World update."""
    # arrange
    w = World(10)
    b = Bot(
        w,
        name="b0",
        position=(0, 0),
    )
    b.velocity = Vector2(1, 0)

    # act
    w.update()

    assert b.pos == Vector2(1 / SIMULATION_FPS, 0)