import imp
from pathlib import Path


def load_plugin(path: str):
    return imp.load_source(Path(path).stem, path)


def reload_plugin(module):
    return imp.reload(module)
