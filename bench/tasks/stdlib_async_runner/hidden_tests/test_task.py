import asyncio
import importlib

import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("runner")


async def delayed(value, delay):
    await asyncio.sleep(delay)
    return value


def test_run_all_order_and_concurrency(mod):
    import time
    start = time.monotonic()
    assert mod.run_all([delayed("a", 0.3), delayed("b", 0.1), delayed("c", 0.2)]) == ["a", "b", "c"]
    assert time.monotonic() - start < 0.55


def test_run_all_twice(mod):
    assert mod.run_all([delayed(1, 0)]) == [1]
    assert mod.run_all([delayed(2, 0)]) == [2]


def test_timeout(mod):
    assert mod.run_with_timeout(delayed("ok", 0.01), 1) == "ok"
    with pytest.raises(TimeoutError):
        mod.run_with_timeout(delayed("slow", 2), 0.1)
