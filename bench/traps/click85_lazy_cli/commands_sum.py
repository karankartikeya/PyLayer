import click


@click.command(name="sum")
@click.argument("numbers", nargs=-1, type=int, required=True)
def sum_cmd(numbers):
    """Sum integers."""
    click.echo(sum(numbers))
