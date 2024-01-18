"""Command line task runners.

`inv -l` to list commands.

"""

from typing import Any

# mypy: ignore-errors

from invoke import task


@task
def f(c_: Any) -> None:
    """Format project."""
    c_.run("ruff format")


@task
def la(c_: Any) -> None:
    """Lint and autofix project."""
    c_.run("ruff check --fix")


@task
def c(c_: Any) -> None:
    """Typecheck with `mypy`."""
    c_.run("mypy .")


@task
def flac(c_: Any) -> None:
    """Format; lint and autofix; typecheck project."""
    f(c_)
    la(c_)
    c(c_)
