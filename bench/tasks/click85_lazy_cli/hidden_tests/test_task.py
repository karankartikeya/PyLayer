import importlib
import sys

import pytest
from click.testing import CliRunner

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def cli_mod():
    for name in ("cli", "commands_greet", "commands_sum"):
        sys.modules.pop(name, None)
    return importlib.import_module("cli")


def test_lazy_import(cli_mod):
    assert "commands_greet" not in sys.modules
    assert "commands_sum" not in sys.modules


def test_greet(cli_mod):
    r = CliRunner().invoke(cli_mod.cli, ["greet", "Ann"])
    assert r.exit_code == 0, r.output
    assert r.output.strip() == "Hello, Ann!"
    r = CliRunner().invoke(cli_mod.cli, ["greet", "Ann", "--shout"])
    assert r.output.strip() == "HELLO, ANN!"


def test_sum(cli_mod):
    r = CliRunner().invoke(cli_mod.cli, ["sum", "1", "2", "39"])
    assert r.exit_code == 0, r.output
    assert r.output.strip() == "42"


def test_help_lists_commands(cli_mod):
    r = CliRunner().invoke(cli_mod.cli, ["--help"])
    assert r.exit_code == 0
    assert "greet" in r.output and "sum" in r.output


def test_unknown_command(cli_mod):
    r = CliRunner().invoke(cli_mod.cli, ["nope"])
    assert r.exit_code == 2
