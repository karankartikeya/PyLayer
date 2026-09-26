"""Check every task discriminates: the reference solution passes its hidden tests, the trap fails.

Usage: uv run python bench/verify_tasks.py [task_id ...]
"""

import shutil
import sys

from run import BENCH, list_tasks, make_workspace, score


def check(task_id: str, kind: str) -> dict:
    src = BENCH / kind / task_id
    if not src.exists():
        return {"pass": None, "test_output": f"no {kind} dir"}
    ws = make_workspace(task_id, f"verify-{kind}", with_venv=False)
    try:
        # An empty traps dir means "the seeded workspace as-is" (e.g. unmigrated code).
        shutil.copytree(src, ws, dirs_exist_ok=True)
        return score(ws, task_id)
    finally:
        shutil.rmtree(ws, ignore_errors=True)


def main() -> None:
    tasks = sys.argv[1:] or list_tasks()
    ok = True
    for task_id in tasks:
        sol, trap = check(task_id, "solutions"), check(task_id, "traps")
        good = sol["pass"] is True and trap["pass"] is False
        ok &= good
        print(f"{'OK  ' if good else 'FAIL'} {task_id:28} solution_pass={sol['pass']} trap_pass={trap['pass']}")
        if sol["pass"] is not True:
            print("   solution output:\n" + sol["test_output"][-1500:])
        if trap["pass"] is not False:
            print("   trap output:\n" + trap["test_output"][-800:])
        elif trap["pass"] is False:
            last = [ln for ln in trap["test_output"].splitlines() if "Error" in ln or "Warning" in ln]
            print(f"   trap fails with: {last[-1].strip()[:150] if last else '?'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
