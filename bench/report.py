"""Print a markdown report from bench/results/results.jsonl.

Usage: uv run python bench/report.py
"""

import json
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
RESULTS = BENCH / "results" / "results.jsonl"
TOOLS = ["get_signature", "typecheck", "run_sandboxed"]


def pct(num: int, den: int) -> str:
    return f"{100 * num / den:.0f}% ({num}/{den})" if den else "-"


def category(task_id: str) -> str:
    meta = BENCH / "tasks" / task_id / "meta.json"
    return json.loads(meta.read_text()).get("category", "?") if meta.exists() else "?"


def main() -> None:
    rows = [json.loads(line) for line in RESULTS.read_text().splitlines()] if RESULTS.exists() else []
    if not rows:
        print("No results yet.")
        return
    arms = sorted({r["arm"] for r in rows})

    print("## Pass rate by arm\n")
    print("| arm | pass rate | avg turns | avg wall (s) | runs with claude error |")
    print("|---|---|---|---|---|")
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        turns = [r["num_turns"] for r in rs if r.get("num_turns") is not None]
        errs = sum(1 for r in rs if r.get("error") or r.get("is_error"))
        print(f"| {arm} | {pct(sum(r['pass'] for r in rs), len(rs))} "
              f"| {sum(turns) / len(turns):.1f} | {sum(r['wall_s'] for r in rs) / len(rs):.0f} | {errs} |"
              if turns else f"| {arm} | {pct(sum(r['pass'] for r in rs), len(rs))} | - | - | {errs} |")

    print("\n## Pass rate by category\n")
    cats = sorted({category(r["task_id"]) for r in rows})
    print("| category | " + " | ".join(arms) + " |")
    print("|---|" + "---|" * len(arms))
    for cat in cats:
        cells = []
        for arm in arms:
            rs = [r for r in rows if r["arm"] == arm and category(r["task_id"]) == cat]
            cells.append(pct(sum(r["pass"] for r in rs), len(rs)))
        print(f"| {cat} | " + " | ".join(cells) + " |")

    b = [r for r in rows if r["arm"] == "B"]
    if b:
        print("\n## PyLayer tool usage (arm B)\n")
        print("| tool | runs using it | avg calls/run |")
        print("|---|---|---|")
        for tool in TOOLS:
            used = sum(1 for r in b if r["tool_calls"].get(tool))
            calls = sum(r["tool_calls"].get(tool, 0) for r in b)
            print(f"| {tool} | {pct(used, len(b))} | {calls / len(b):.1f} |")
        none = sum(1 for r in b if not r["tool_calls"])
        print(f"\nRuns with no PyLayer calls at all: {pct(none, len(b))}")

    per_task: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        per_task[r["task_id"]][r["arm"]].append(r["pass"])

    print("\n## Per task\n")
    print("| task | category | " + " | ".join(arms) + " |")
    print("|---|---|" + "---|" * len(arms))
    disagree = []
    for task_id in sorted(per_task):
        rates = {arm: per_task[task_id].get(arm, []) for arm in arms}
        cells = [f"{sum(v)}/{len(v)}" if v else "-" for v in rates.values()]
        print(f"| {task_id} | {category(task_id)} | " + " | ".join(cells) + " |")
        if "A" in rates and "B" in rates and rates["A"] and rates["B"]:
            if sum(rates["A"]) / len(rates["A"]) != sum(rates["B"]) / len(rates["B"]):
                disagree.append((task_id, cells))

    print("\n## Tasks where A and B disagree\n")
    if disagree:
        for task_id, cells in disagree:
            print(f"- {task_id}: " + ", ".join(f"{a}={c}" for a, c in zip(arms, cells)))
    else:
        print("None.")


if __name__ == "__main__":
    main()
