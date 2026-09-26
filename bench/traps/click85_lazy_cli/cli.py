import importlib

import click

COMMANDS = {"greet": "commands_greet:greet", "sum": "commands_sum:sum_cmd"}


class LazyGroup(click.MultiCommand):
    def __init__(self, *args, lazy_commands: dict[str, str], **kwargs):
        super().__init__(*args, **kwargs)
        self.lazy_commands = lazy_commands

    def list_commands(self, ctx):
        return sorted(set(self.lazy_commands))

    def get_command(self, ctx, cmd_name):
        if cmd_name in self.lazy_commands:
            module_name, attr = self.lazy_commands[cmd_name].split(":")
            return getattr(importlib.import_module(module_name), attr)
        return None


@click.group(cls=LazyGroup, lazy_commands=COMMANDS)
def cli():
    """Lazy CLI."""
