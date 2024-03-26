"""Command line task runners.

`inv {task}` to run a task.
`inv -l` to list tasks.
"""

from typing import Any

# mypy: ignore-errors
from invoke import task


@task
def fmt(c: Any) -> None:
    """Format project with Ruff."""
    print("Formatting with Ruff...")
    c.run("ruff format")


@task
def lint(c: Any) -> None:
    """Lint and autofix project with Ruff; typecheck project with Mypy."""
    print("Linting and auto-fixing with Ruff...")
    c.run("ruff check --fix")
    print("Type checking with Mypy...")
    c.run("mypy .")


@task
def fl(c: Any) -> None:
    """Format; lint and autofix; typecheck project."""
    fmt(c)
    lint(c)
