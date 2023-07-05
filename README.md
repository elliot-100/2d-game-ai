# 2d-game-ai

Experimental Python project to explore video game-style 'AI' behaviour in a 2D
environment.

Intended to focus on simulated entities' (`Bot`) behaviour at an 'action'/'tactical'
level, e.g. searching, spotting, assessing and attacking.

Functional decisions:

- Bot is initially stationary.
- Bot is either stationary or moving at a constant speed.
- Bot can only moving in the direction it is facing.
- Bot can rotate at a constant rate.
- Bot is modelled as a point.

To be decided:

- Can Bot rotate while moving, i.e. constant speed but varying velocity?
