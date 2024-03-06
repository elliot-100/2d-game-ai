"""Command line task runners.

`inv -l` to list commands.

"""

from typing import Any

# mypy: ignore-errors
from invoke import task


@task
def fmt(c: Any) -> None:
    """Format project."""
    c.run("ruff format")


@task
def lint(c: Any) -> None:
    """Lint and autofix; typecheck project."""
    c.run("ruff check --fix")
    c.run("mypy .")


@task
def fl(c: Any) -> None:
    """Format; lint and autofix; typecheck project."""
    fmt(c)
    lint(c)
