"""get_signature: introspect a dotted path using the *project's* interpreter."""

import json
import subprocess

from pylayer.project import resolve_project_dir, resolve_python

TIMEOUT_S = 10

# Runs inside the project's interpreter. Prints one JSON object to stdout.
INTROSPECT_SCRIPT = r'''
import difflib, importlib, importlib.metadata as md, inspect, json, sys, warnings

# Record deprecation warnings raised while importing/resolving the target
# (e.g. click.MultiCommand is served by a module __getattr__ that warns).
_warn_ctx = warnings.catch_warnings(record=True)
_caught = _warn_ctx.__enter__()
warnings.simplefilter("always")

target = sys.argv[1]
parts = target.split(".")
out = {"target": target, "exists": False}

def package_info(top):
    try:
        dists = md.packages_distributions().get(top) or [top]
        return dists[0], md.version(dists[0])
    except Exception:
        return top, None

def public(names):
    return [n for n in names if not n.startswith("_")]

def emit():
    kinds = (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    msgs = []
    for w in _caught:
        if issubclass(w.category, kinds):
            m = f"{w.category.__name__}: {str(w.message).strip()[:300]}"
            if m not in msgs:
                msgs.append(m)
    if msgs:
        out["warnings"] = msgs[:3]
    print(json.dumps(out))

def deprecation(o):
    # PEP 702 (@deprecated) sets __deprecated__; pydantic v2 uses it for v1-era methods.
    msg = getattr(o, "__deprecated__", None)
    return str(msg)[:300] if isinstance(msg, str) else None

# Import the longest importable module prefix.
obj, depth, import_error = None, 0, None
for i in range(len(parts), 0, -1):
    try:
        obj = importlib.import_module(".".join(parts[:i]))
        depth = i
        break
    except ModuleNotFoundError as e:
        import_error = str(e)
    except Exception as e:
        import_error = f"{type(e).__name__}: {e}"
        break

out["package"], out["version"] = package_info(parts[0])

if obj is None:
    out["error"] = import_error
    emit()
    sys.exit(0)

# Walk remaining attributes.
missing = None
for name in parts[depth:]:
    try:
        obj = getattr(obj, name)
        depth += 1
    except AttributeError as e:
        missing = name
        out["attribute_error"] = str(e)[:500]
        break

if missing is not None:
    parent_path = ".".join(parts[:depth])
    candidates = public(dir(obj)) if not missing.startswith("_") else dir(obj)
    matches = difflib.get_close_matches(missing, candidates, n=5, cutoff=0.5)
    if len(matches) < 5:
        # Fallback: substring matches catch e.g. parse_obj_v3 -> model_validate misses,
        # but also parse_obj when a suffix was invented.
        stem = missing.split("_")[0].lower()
        for c in candidates:
            if stem and stem in c.lower() and c not in matches:
                matches.append(c)
            if len(matches) >= 5:
                break
    # Non-deprecated suggestions first, so we don't steer toward legacy APIs.
    deprecated = {m for m in matches if deprecation(getattr(obj, m, None))}
    matches.sort(key=lambda m: m in deprecated)
    out.update(nearest_parent=parent_path, missing=missing,
               suggestions=[f"{parent_path}.{m}" + (" (deprecated)" if m in deprecated else "")
                            for m in matches])
    emit()
    sys.exit(0)

out["exists"] = True
dep = deprecation(obj)
if dep:
    out["deprecated"] = dep
if inspect.ismodule(obj):
    out["kind"] = "module"
elif inspect.isclass(obj):
    out["kind"] = "class"
elif callable(obj):
    out["kind"] = "function"
else:
    out["kind"] = "attribute"
    out["value_repr"] = repr(obj)[:200]

if out["kind"] in ("class", "function"):
    try:
        out["signature"] = str(inspect.signature(obj))
    except (TypeError, ValueError):
        out["signature"] = None

doc = inspect.getdoc(obj) if out["kind"] != "attribute" else None
if doc:
    out["doc"] = "\n".join(doc.splitlines()[:15])

if out["kind"] == "class":
    out["members"] = public(dir(obj))[:150]
elif out["kind"] == "module":
    out["members"] = public(dir(obj))[:150]

emit()
'''


def get_signature(target: str, project_dir: str | None = None) -> dict:
    proj = resolve_project_dir(project_dir)
    try:
        python = resolve_python(proj)
    except FileNotFoundError as e:
        return {"target": target, "exists": False, "error": str(e)}

    try:
        proc = subprocess.run(
            [str(python), "-c", INTROSPECT_SCRIPT, target],
            cwd=proj,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return {"target": target, "exists": False, "error": f"introspection timed out after {TIMEOUT_S}s"}

    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {
            "target": target,
            "exists": False,
            "error": f"introspection failed (exit {proc.returncode}): {proc.stderr[-1500:]}",
        }
    result["interpreter"] = str(python)
    return result
