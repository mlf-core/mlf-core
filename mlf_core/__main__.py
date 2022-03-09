#!/usr/bin/env python
"""Command-line interface."""
import click
from rich import traceback


@click.command()
@click.version_option(version="1.11.3", message=click.style("mlf-core Version: 1.11.3"))
def main() -> None:
    """mlf-core."""


if __name__ == "__main__":
    traceback.install()
    main(prog_name="mlf-core")  # pragma: no cover
