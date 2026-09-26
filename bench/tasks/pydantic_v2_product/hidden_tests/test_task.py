import importlib
import json
from decimal import Decimal

import pytest

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture
def mod():
    return importlib.import_module("catalog")


def good(**kw):
    d = {"sku": "ABC-1234", "tags": ["x"], "price": "19.90"}
    d.update(kw)
    return d


def test_valid(mod):
    p = mod.parse_product(good())
    assert p.price == Decimal("19.90")
    assert json.loads(mod.product_json(p))["price"] == "19.90"
    assert json.loads(mod.product_json(p))["sku"] == "ABC-1234"


@pytest.mark.parametrize("bad", [
    {"sku": "abc-1234"}, {"sku": "ABC-123"}, {"sku": "ABCD-1234"}, {"sku": "xABC-1234"},
    {"tags": []}, {"tags": list("abcdef")}, {"price": "0"}, {"price": "-1"},
])
def test_invalid(mod, bad):
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        mod.parse_product(good(**bad))
