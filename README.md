# 2d-game-ai

Experimental Python project to explore video game-style 'AI' behaviour in a 2D top-down
environment.

Intended to focus on simulated 'Bot' entities'  behaviour at an 'action'/'tactical'
level, e.g. searching, spotting, assessing and attacking.

Python isn't the best tool for this, but it's largely a learning exercise.

Implemented as a library. User interface uses [pygame-ce](https://pyga.me/).


## Example

```
# Namespace may change...
from two_d_game_ai import Vector2
from two_d_game_ai.entities import Bot
from two_d_game_ai.render.view import View
from two_d_game_ai.world import World

# WORLD

# Create a World
the_world = World(100)

# ENTITIES

# Add a Bot to the World...
b0 = Bot(
    name="b0",
    world=the_world,
    pos=Vector2(20, 20),
)

# Add another Bot to the World...
b1 = Bot(
    name="b1",
    world=the_world,
    pos=Vector2(0, 0),
)

# ... with a destination
b1.destination = Vector2(25, -50)

# Create a View to the World.
# Provides user interface, but not required: e.g. Bot, World test suites don't have one.

view = View(
    name="the_view",
    world=the_world,
    scale_factor=2,
)

# MAIN LOOP

while view.running:
    view.handle_inputs()
    if not the_world.is_paused:
        the_world.update()
    view.render()
```


### World

- Circular (for now)
- Origin (0, 0) at centre
- Uses Vector2 class for coordinates

### Bot

- Treated as a point
- Initially stationary
- While stationary, can rotate at a constant rate
- Can move at a constant rate in the direction it is facing
- Can be given a single destination; will move to it
- Can see Bots it's facing
- Keeps track of visible and known (previously visible) other Bots


### View


#### World

- Centered on origin; conventional (positive, right-handed, y-axis up) coordinate system
- By default, 1 World unit : 1 display pixel; can be scaled at initialisation
- Updates initially paused, P key toggles pause
- Renders every update at up to 60 updates/second; is allowed to lag, i.e. may run slower than real-time.


#### Bots

- Renders all Bots as icons
  - Direction indicator
  - Vision cone
  - Can-see and knows-about relationships as lines
- Primary mouse click to select a Bot; secondary mouse click to set a destination

## Development

- [Invoke](https://www.pyinvoke.org/) can be used for CLI tasks (autoformatting, linting
and type checking).
  `invoke --list` or `inv -l` to get a list of tasks.
