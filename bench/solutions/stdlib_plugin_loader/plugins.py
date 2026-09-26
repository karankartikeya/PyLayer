import importlib.util
import sys
from pathlib import Path


def _exec_from_file(name: str, path: str, module=None):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load plugin from {path}")
    if module is None:
        module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_plugin(path: str):
    return _exec_from_file(Path(path).stem, path)


def reload_plugin(module):
    # importlib.reload() can't find specs for modules loaded from arbitrary paths; re-exec from the file.
    return _exec_from_file(module.__name__, module.__file__, module)
