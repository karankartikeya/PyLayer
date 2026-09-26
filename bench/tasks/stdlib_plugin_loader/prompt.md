Create `plugins.py` (standard library only; we target Python 3.12) with:

- `load_plugin(path: str)`: loads a Python source file from an arbitrary filesystem path as a module (module name = the file's stem) and returns the module.
- `reload_plugin(module)`: re-executes the plugin from its file and returns the refreshed module.
