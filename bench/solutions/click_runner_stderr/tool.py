from pathlib import Path

import click
from click.testing import CliRunner


@click.command()
@click.argument("path")
def main(path: str) -> None:
    p = Path(path)
    if not p.exists():
        click.echo(f"error: no such file: {path}", err=True)
        raise SystemExit(1)
    with p.open() as f:
        click.echo(sum(1 for _ in f))


def run_cli(args: list[str]) -> tuple[str, str, int]:
    result = CliRunner().invoke(main, args)
    return result.stdout, result.stderr, result.exit_code
