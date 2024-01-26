

def test_is_outside_world_bounds() -> None:
    """Test that Bots are inside/outside World."""
    w = World(10)
    b0 = Bot(
        world=w,
        name="b0",
        pos=Vector2(5, -5),
    )
    b1 = Bot(
        world=w,
        name="b0",
        pos=Vector2(-8, 9),
    )
    assert not b0.is_outside_world_bounds
    assert b1.is_outside_world_bounds
