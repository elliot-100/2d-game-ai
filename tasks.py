"""Command line task runners using Invoke.

`inv {task}` to run a task.
`inv -l` to list tasks.
"""

from typing import Any

# mypy: ignore-errors
from invoke import task


@task
def fmt(c: Any) -> None:
    """Format project with Ruff."""
    print("🖌️ Formatting with Ruff...")
    c.run("ruff format")


@task
def lint(c: Any) -> None:
    """Lint and autofix project with Ruff; typecheck project with Mypy."""
    print("🩺️ Linting and auto-fixing with Ruff...")
    c.run("ruff check --fix --output-format=concise")
    print("🔬 Type checking with Mypy...")
    c.run("mypy .")


@task
def fl(c: Any) -> None:
    """Format; lint and autofix; typecheck project."""
    fmt(c)
    lint(c)


@task
def doc(c: Any, *, build: bool = False) -> None:
    """Start local pdoc server, or build docs."""
    if build:
        print("Building docs at /docs/index.html...")
        c.run("pdoc two_d_game_ai -d numpy -o docs")
    else:
        print("Opening pdoc server at http://localhost:8080...")
        c.run("pdoc two_d_game_ai -d numpy")
