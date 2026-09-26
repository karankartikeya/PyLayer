Create `runner.py` with two synchronous helpers for calling async code from ordinary (non-async) code, where no event loop is running:

- `run_all(coros: list) -> list`: runs the given coroutines concurrently and returns their results in order.
- `run_with_timeout(coro, seconds: float)`: returns the coroutine's result, or raises `TimeoutError` if it takes longer than `seconds`.

Standard library only. We target Python 3.12 and CI treats DeprecationWarnings as errors.
