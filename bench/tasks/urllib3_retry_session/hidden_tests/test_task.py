import importlib

import pytest
import requests
from urllib3.util.retry import Retry


@pytest.fixture
def mod():
    return importlib.import_module("http_session")


@pytest.mark.parametrize("url", ["https://example.com/x", "http://example.com/x"])
def test_retry_config(mod, url):
    s = mod.make_session(retries=4)
    assert isinstance(s, requests.Session)
    r = s.get_adapter(url).max_retries
    assert isinstance(r, Retry)
    assert r.total == 4
    assert {"GET", "PUT", "POST"} <= {m.upper() for m in r.allowed_methods}
    assert {502, 503, 504} <= set(r.status_forcelist)
    assert r.backoff_factor == 0.5


def test_default_retries(mod):
    assert mod.make_session().get_adapter("https://e.com").max_retries.total == 3
