# PyLayer: results

**Question.** Does giving Claude Code three grounding tools (`get_signature`, `typecheck`, `run_sandboxed`) raise its pass rate on Python tasks where the installed library versions matter?

**Answer.** It depends on the model:

- **Haiku: yes.** Pass rate goes from **60% to 96%**. The cost per correct answer stays about the same.
- **Sonnet 5: no meaningful gain.** It already passes 98% without the tools, reaches 100% with them, and each correct answer costs 60% more.
- **Haiku with PyLayer nearly matches Sonnet without it** (96% vs 98%), at **less than half the cost per correct answer** ($0.071 vs $0.161).

## Setup

- **30 tasks**, each a normal developer request with pinned dependencies. Each task depends on a real version difference:
  - removed or renamed APIs: pydantic v1/v2, SQLAlchemy 1.4/2.0, NumPy 2.x, pandas 2/3, Starlette 1.0, marshmallow 4, click 8.2+, httpx 0.28, urllib3 2, Python 3.12 stdlib;
  - hidden transitive pins, e.g. `fastapi==0.99` quietly installs pydantic v1;
  - private packages the model can't have seen, one with stale docs and one with no docs;
  - two multi-file migrations.
- **Every task is verified.** A reference solution passes the hidden tests and a deliberately outdated trap solution fails them (`bench/verify_tasks.py`).
- **Two arms**, run headless in a fresh workspace with the pinned venv:
  - **A (baseline):** Claude Code with file tools and `python`.
  - **B (PyLayer):** the same, plus the PyLayer MCP server and a 3-sentence `CLAUDE.md` asking Claude to use it.
- **Scoring:** hidden tests, never seen by Claude, run in a network-less Docker sandbox.
- **Volume:** 2 models × 30 tasks × 2 arms × 3 repeats = **360 runs**.

## Results

| | Baseline (A) | PyLayer (B) | Paired A vs B |
|---|---|---|---|
| **Haiku** | 60% (54/90, 95% CI 50–70%) | **96%** (86/90, 95% CI 89–98%) | B-only passes 33, A-only 1, p = 4×10⁻⁹ |
| **Sonnet 5** | 98% (88/90, 95% CI 92–99%) | 100% (90/90, 95% CI 96–100%) | B-only passes 2, A-only 0, p = 0.5 |

The paired comparison matches each A run to the B run with the same task and repeat. The p-value is an exact McNemar test.

| | Avg turns | Avg time | Est. cost per correct answer |
|---|---|---|---|
| Haiku, A | 4.2 | 25s | $0.069 |
| Haiku, B | 11.3 | 41s | $0.071 |
| Sonnet 5, A | 6.6 | 34s | $0.161 |
| Sonnet 5, B | 12.1 | 42s | $0.257 |

Costs are Claude Code's own estimates (`total_cost_usd`), not billed amounts.

## Why it works

Haiku's 36 baseline failures, by cause:

| Cause | Baseline failures | PyLayer failures |
|---|---|---|
| Removed parameter (`missing=`, `proxies=`, `mix_stderr=`, `regex=` …) | 9 | 0 |
| Deprecated API that fails when CI treats warnings as errors | 8 | 1 |
| Missing module or import name (`pydantic_settings`, `ledgerkit.errors`, `imp` …) | 6 | 0 |
| Missing attribute or method (`np.trapz` in 2.5, `Ledger.move` …) | 3 | 0 |
| Removed alias (pandas `'M'`, `'T'`, `'H'`) | 2 | 0 |
| Behaviour change (pydantic v2 `Optional` becomes required) | 4 | 3 |
| Wrong result / other | 4 | 0 |

- **78% of baseline failures (28 of 36) come from using an API from the wrong version.** PyLayer brings that to 1.
- The typical baseline failure takes about 2 turns: Haiku writes code from memory and stops. With PyLayer, `get_signature` shows it the installed version's real API, and `typecheck`/`run_sandboxed` catch whatever slips through.
- **Sonnet 5 already checks versions on its own.** It reads the pins, looks inside the installed packages, and runs the code. PyLayer duplicates that work, so it only adds turns.

## What PyLayer does not fix

1. **Behaviour changes with no test covering them.** In the `migrate_app` task, every Haiku run in both arms migrated correctly except one point: pydantic v2 turns `Optional[str]` without a default into a required field. The visible tests didn't cover that case, and no tool flags it.
2. **Warnings that don't fail the run.** One PyLayer run saw pandas' `Pandas4Warning` in the sandbox output but moved on, because the exit code was 0.
3. **Soft enforcement isn't guaranteed.** Haiku skipped the tools entirely in 3 of 90 PyLayer runs.
4. **Type-checker noise on untyped libraries.** SQLAlchemy 1.4 produces false-positive type errors. Claude ignored them, but they cost turns.

## Limits of this study

- 30 tasks and 3 repeats. The Haiku effect is large and consistent across repeats, but individual task rates are noisy.
- Every task has a version trap by design. Real workloads contain fewer, so real-world gains will be smaller than +36 points.
- Only one prompt, one enforcement style (soft) and two models were tested.

## Suggested next steps

1. **Add a warnings-as-errors option to `run_sandboxed`**, or report warnings separately from the exit code (fixes gap 2).
2. **Test hard enforcement** with Claude Code hooks that run `typecheck` after every edit (gap 3).
3. **Position PyLayer as the thing that makes cheap models reliable**, and compare Haiku with PyLayer against Sonnet on cost per correct answer for real workloads.

## Reproduce

```sh
uv sync
uv run python bench/verify_tasks.py                          # 30/30 tasks discriminate
uv run python bench/run.py --arms A,B --repeats 3            # Sonnet (default model)
uv run python bench/run.py --arms A,B --repeats 3 --model haiku
uv run python bench/analyze.py                               # the numbers above
```
