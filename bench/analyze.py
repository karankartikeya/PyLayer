"""Final analysis: pass rates with confidence intervals, paired A/B comparison, failure causes, cost per pass.

Usage: uv run python bench/analyze.py
"""

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parent
RESULTS = BENCH / "results" / "results.jsonl"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value on discordant pairs (b = only B passed, c = only A passed)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def failure_cause(output: str) -> str:
    summary = " ".join(line for line in output.splitlines() if line.startswith(("FAILED", "ERROR", "E ")))
    text = summary or output
    if re.search(r"Pandas4Warning|FutureWarning|DeprecationWarning|PydanticDeprecated", text):
        return "deprecated API (fails under warnings-as-errors)"
    if re.search(r"unexpected keyword argument|PydanticUserError|is removed", text):
        return "removed parameter"
    if re.search(r"ModuleNotFoundError|ImportError|cannot import name", text):
        return "missing module / import name"
    if re.search(r"AttributeError", text):
        return "missing attribute / method"
    if re.search(r"Invalid frequency|ValueError", text):
        return "removed alias / invalid value"
    if re.search(r"ValidationError", text):
        return "behaviour change (validation)"
    if re.search(r"assert", text):
        return "wrong result"
    return "other"


def meta(task_id: str) -> dict:
    return json.loads((BENCH / "tasks" / task_id / "meta.json").read_text())


def pct(k: int, n: int) -> str:
    lo, hi = wilson(k, n)
    return f"{100 * k / n:.0f}% ({k}/{n}, 95% CI {100 * lo:.0f}-{100 * hi:.0f}%)" if n else "-"


def main() -> None:
    rows = [json.loads(line) for line in RESULTS.read_text().splitlines()]
    models = sorted({r.get("model_arg", "default") for r in rows})

    print("# PyLayer benchmark: final analysis\n")
    for model in models:
        rs = [r for r in rows if r.get("model_arg", "default") == model]
        tasks = sorted({r["task_id"] for r in rs})
        repeats = sorted({r["repeat"] for r in rs})
        label = "Sonnet 5 (default)" if model == "default" else model
        print(f"## Model: {label}\n")
        print(f"{len(tasks)} tasks, repeats {repeats}, {len(rs)} runs.\n")

        print("| arm | pass rate | avg turns | avg wall (s) | est. cost total | est. cost per pass |")
        print("|---|---|---|---|---|---|")
        for arm in ("A", "B"):
            a = [r for r in rs if r["arm"] == arm]
            k = sum(r["pass"] for r in a)
            cost = sum(r.get("total_cost_usd") or 0 for r in a)
            turns = sum(r.get("num_turns") or 0 for r in a) / len(a)
            wall = sum(r["wall_s"] for r in a) / len(a)
            print(f"| {arm} | {pct(k, len(a))} | {turns:.1f} | {wall:.0f} | ${cost:.2f} | "
                  f"{'$%.3f' % (cost / k) if k else '-'} |")

        # Paired comparison on identical (task, repeat).
        by_key = {(r["task_id"], r["repeat"], r["arm"]): r["pass"] for r in rs}
        pairs = [(by_key[(t, rep, "A")], by_key[(t, rep, "B")]) for t in tasks for rep in repeats
                 if (t, rep, "A") in by_key and (t, rep, "B") in by_key]
        both = sum(1 for a, b in pairs if a and b)
        only_b = sum(1 for a, b in pairs if b and not a)
        only_a = sum(1 for a, b in pairs if a and not b)
        neither = sum(1 for a, b in pairs if not a and not b)
        print(f"\nPaired runs: {len(pairs)}. Both pass {both}, only PyLayer passes **{only_b}**, "
              f"only baseline passes **{only_a}**, both fail {neither}. "
              f"Exact McNemar p = {mcnemar_exact(only_b, only_a):.2g}.\n")

        print("| set | A | B |")
        print("|---|---|---|")
        for tset in ("v1", "hard", "ext"):
            cells = []
            for arm in ("A", "B"):
                a = [r for r in rs if r["arm"] == arm and meta(r["task_id"]).get("set", "v1") == tset]
                cells.append(f"{sum(r['pass'] for r in a)}/{len(a)}" if a else "-")
            print(f"| {tset} | {cells[0]} | {cells[1]} |")

        print("\n### Why runs failed\n")
        print("| cause | A failures | B failures |")
        print("|---|---|---|")
        causes: dict[str, Counter] = defaultdict(Counter)
        for r in rs:
            if not r["pass"]:
                out = (REPO / r["artifact_dir"] / "test_output.txt").read_text()
                causes[r["arm"]][failure_cause(out)] += 1
        for cause in sorted(set(causes["A"]) | set(causes["B"]), key=lambda c: -(causes["A"][c] + causes["B"][c])):
            print(f"| {cause} | {causes['A'][cause]} | {causes['B'][cause]} |")

        b_runs = [r for r in rs if r["arm"] == "B"]
        no_tools = [r for r in b_runs if not r["tool_calls"]]
        print(f"\nArm B runs that made no PyLayer calls: {len(no_tools)}/{len(b_runs)} "
              f"(passed {sum(r['pass'] for r in no_tools)}).")
        tool_totals = Counter()
        for r in b_runs:
            tool_totals.update(r["tool_calls"])
        print("Tool calls per arm-B run: " + ", ".join(f"{t} {n / len(b_runs):.1f}" for t, n in tool_totals.most_common()))

        print("\n### Per task (passes / runs)\n")
        print("| task | set | category | A | B |")
        print("|---|---|---|---|---|")
        for t in sorted(tasks, key=lambda t: (meta(t).get("set", "v1"), t)):
            cells = []
            for arm in ("A", "B"):
                a = [r for r in rs if r["task_id"] == t and r["arm"] == arm]
                cells.append(f"{sum(r['pass'] for r in a)}/{len(a)}")
            m = meta(t)
            print(f"| {t} | {m.get('set', 'v1')} | {m['category']} | {cells[0]} | {cells[1]} |")
        print()


if __name__ == "__main__":
    main()
