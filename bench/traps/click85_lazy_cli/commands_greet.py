import click


@click.command()
@click.argument("name")
@click.option("--shout", is_flag=True)
def greet(name, shout):
    """Greet someone."""
    msg = f"Hello, {name}!"
    click.echo(msg.upper() if shout else msg)
