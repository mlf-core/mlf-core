#!/usr/bin/env python
"""Command-line interface."""
import click
from rich import traceback


@click.command()
@click.version_option()
def main() -> None:
    """mlf-core."""


if __name__ == "__main__":
    traceback.install()
    main(prog_name="mlf-core")  # pragma: no cover
