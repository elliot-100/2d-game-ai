# 2d-game-ai

Experimental Python project to explore video game-style 'AI' behaviour in a 2D top-down
environment.

Intended to focus on simulated 'Bot' entities'  behaviour at an 'action'/'tactical'
level, e.g. searching, spotting, assessing and attacking.

Python isn't the best tool for this, but it's largely a learning exercise.

Implemented as a library. User interface uses [pygame-ce](https://pyga.me/).


## Example

```python
from two_d_game_ai.entities.bot import Bot
from two_d_game_ai.view.view import View
from two_d_game_ai.world.world import World

# WORLD

# Create a World
the_world = World(
  size=300,
  grid_size=16,
)

# ENTITIES

# Add a Bot to the World...
b0 = Bot(position_from_sequence=(20, 20))
the_world.add_entity(b0)

# ... with a destination
b0.destination = (25, -50)

# Create a View to the World.
# Provides user interface, but not required: e.g. Bot, World test suites don't have one.

view = View(world=the_world)

# MAIN LOOP

while view.running:
  view.handle_inputs()
  if not the_world.is_paused:
    the_world.update()
  view.render()
```


### World

- Square
- Divided into a square Grid


### Obstacles

- Circular or rectangular entities that block Bot movement


### Bot

- Treated as a point
- Initially stationary
- While stationary, can rotate at a constant rate
- Can move at a constant rate in the direction it is facing
- Can be given a destination; will plan and follow a route to it
- Can see Bots it's facing
- Keeps track of visible and known (previously visible) other Bots


### View

#### Displays World:

- Centered on origin (0, 0); conventional (positive, right-handed, y-axis up) coordinate system
- By default, 16 display units : 1 world unit; can be scaled at initialisation
- Initially paused, P key toggles pause
- Renders every update at up to 60 updates/second; is permitted to lag, i.e. may run slower than real-time.

#### Displays Bots:

- As icons with:
  - Direction indicator
  - Destination point and waypoints on a calculated route
  - Vision cone
  - Can-see and knows-about relationships as lines
- Primary mouse click to select a Bot; secondary mouse click to set a destination


## Development

- [Invoke](https://www.pyinvoke.org/) can be used for CLI tasks (autoformatting, linting
and type checking).
  `invoke --list` or `inv -l` to get a list of tasks.
