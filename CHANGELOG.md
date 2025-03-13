# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

As an application, does not attempt to adhere to Semantic Versioning.

Historic and pre-release versions aren't necessarily included.


## [0.6.0] - 2025-03-13

### Added:

- Documentation:
  - in source `/docs`
  - `inv doc` to open docs in browser (local pdoc server); `-b` to build docs  
- View: render Grid untraversable cells; Bot path between waypoints

### Changed:

- Bot pathfinding:
  - Ignore destination setting if an untraversable cell
  - Direct route if there's a line-of-sight to destination
  - Simplify route by removing collinear points
- Revise and explicitly declare API
- View: anti-alias most graphics; other rendering improvements
- Deps: require pygame-ce >=2.5.0


## [0.5.0] - 2024-09-26

### Added

- Bot pathfinding:
  - World grid of variable resolution
  - MovementBlocks
  - Bots plan all routes on the World grid and route around MovementBlocks
- View: margin around rendered World; render Grid, MovementBlock, Bot waypoints
- Dev dependency pdoc

### Changed

- World is now square
- Bot pathfinding: destination can't be set outside World limits
- Colour palette
- Simplify dependencies by using `=>` instead of `^`


## [0.4.0] - 2024-05-14

### Added

- View: user can select a Bot with primary mouse button; set destination with secondary mouse button
- View: World is initially paused; user can toggle pause with P key
- View: draw Bot vision cone indicator (doesn't reflect infinite vision range)
- View: draw World origin
- `Invoke` tasks for linting/formatting (ruff) and type checking (mypy)

### Fixed

- Bot: exception if name wasn't a string
- View: Bot nose indicator wasn't scaled to display
- Mypy warning: `--strict-concatenate is deprecated ...`

### Changed

- Bot `.pos` and `.destination` take `tuple[float, float]` instead of `Vector2`
- World is rectangular
- CI: use ruff format instead of black + isort
- Upgrade dev/test dependencies: pytest, ruff
- Remove `poetry.lock` from repo for now

### Removed

- Dev/test/CI dependencies: black, isort


## [0.3.0] - 2024-01-08

### Added

- Bot keeps track of visible and known (but no-longer visible) others
- View renders can-see and knows-about relationships as lines
- View scaling
- Introduced Observer pattern for Bot and View
- Trivial logging

### Fixed

- Bot ignored own position when calculating bearing to destination
- Illegal package name

### Changed

- Bots are now created in their own right, with reference to World, instead of World
  method: `Bot(the_world, ...)` instead of `World.add_bot(...)`
- Upgrade dependency: pygame-ce to >=2.4.0
- Upgrade dev/test dependencies: black, mypy, pytest, pre-commit, ruff
- Upgrade CI dependencies: actions/setup-python


## [0.2.0] - 2023-09-06

Baseline release.

[0.6.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/elliot-100/2d-game-ai/releases/tag/v0.2.0
