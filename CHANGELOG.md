# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

As an application, does not attempt to adhere to Semantic Versioning.

Historic and pre-release versions aren't necessarily included.


## [UNRELEASED] - TBC

### Added

- Draw Bot vision cone indicator (doesn't reflect infinite vision range)
- `Invoke` tasks for linting/formatting (ruff) and type checking (mypy)

### Fixed

- Mypy warning: `--strict-concatenate is deprecated ...`

### Changed

- Refactor bearing calculations, colours, draw/blit calls
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

[0.3.0]: https://github.com/elliot-100/2d-game-ai/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/elliot-100/2d-game-ai/releases/tag/v0.2.0
