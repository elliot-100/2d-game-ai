# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

As an application, does not attempt to adhere to Semantic Versioning.

Historic and pre-release versions aren't necessarily included.


## [UNRELEASED] - TBC

### Added

- MovementBlock entity: circular, Bots stop when they are about to collide with it
- Dev dependency pdoc

### Fixed

-

### Changed

- Simplify dependencies by using `=>` instead of `^`

### Removed

-


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
- Extensive refactors
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
- CHANGELOG.md (this document)

### Fixed

- Bot ignored own position when calculating bearing to destination
- Illegal package name

### Changed

- Bots are now created in their own right, with reference to World, instead of World
  method: `Bot(the_world, ...)` instead of `World.add_bot(...)`
- Refactor: extract `render` package and `render.BotRenderer` class
- Tighten ruff config
- Upgrade dependency: pygame-ce to 2.4.0
- Upgrade dev/test dependencies: black, mypy, pytest, pre-commit, ruff
- Upgrade CI dependencies: actions/setup-python


## [0.2.0] - 2023-09-06

Baseline release.

[0.4.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/elliot-100/2d-game-ai/releases/tag/v0.2.0
