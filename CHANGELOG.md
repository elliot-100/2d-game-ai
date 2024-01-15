# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

As an application, does not attempt to adhere to Semantic Versioning.

Historic and pre-release versions aren't necessarily included.


## [UNRELEASED] - TBC

### Added

- Bot keeps track of visible and known (but no-longer visible) others
- View renders can-see and knows-about relationships as lines
- Introduced Observer pattern for Bot and View
- CHANGELOG.md (this document)
- Trivial logging

### Fixed

- Bot ignored own position when calculating bearing to destination
- Illegal package name

### Changed

- Upgrade dependency: pygame-ce to 2.4.0
- Upgrade dev/test dependencies: black, mypy, pytest, pre-commit, ruff
- Tighten ruff config
- Upgrade CI dependencies: actions/setup-python


## [0.2.0] - 2023-09-06

Baseline release.

[UNRELEASED]: https://github.com/elliot-100/2d-game-ai/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/elliot-100/2d-game-ai/releases/tag/v0.2.0
