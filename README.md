# 2d-game-ai

Experimental Python project to explore video game-style 'AI' behaviour in a 2D top-down
environment.

Intended to focus on simulated 'Bot' entities'  behaviour at an 'action'/'tactical'
level, e.g. searching, spotting, assessing and attacking.


## World/simulation behaviour

- Nominally 60 updates/second, but see below.


## Bot behaviour

- Modelled as a point
- Initially stationary
- While stationary, can rotate at a constant rate
- Can move at a constant rate in the direction it is facing
- Can be given a destination; will move to it
- Keeps track of visible and known (but no-longer visible) others


## View/renderer behaviour

- Displays all Bots
- Renders every World update; is allowed to lag, i.e. may run slower than real-time.
- Renders can-see and knows-about relationships as lines
