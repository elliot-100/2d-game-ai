# 2d-game-ai

Experimental Python project to explore video game-style 'AI' behaviour in a 2D top-down
environment.

Intended to focus on simulated 'Bot' entities'  behaviour at an 'action'/'tactical'
level, e.g. searching, spotting, assessing and attacking.


## Behaviour


### World/simulation

- Nominally 60 updates/second, but see below.


### Bot

- Modelled as a point
- Initially stationary
- While stationary, can rotate at a constant rate
- Can move at a constant rate in the direction it is facing
- Can be given a destination; will move to it
- Keeps track of visible and known (but no-longer visible) others


### View/renderer

- Displays all Bots
- Renders every World update; is allowed to lag, i.e. may run slower than real-time.
- Renders can-see and knows-about relationships as lines
- Can be scaled

## Development

- [Invoke](https://www.pyinvoke.org/) can be used for CLI tasks (autoformatting, linting
and type checking).
  `invoke --list` or `inv -l` to get a list of tasks.
