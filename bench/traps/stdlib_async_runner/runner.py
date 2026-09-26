import asyncio


def run_all(coros: list) -> list:
    loop = asyncio.get_event_loop()
    return list(loop.run_until_complete(asyncio.gather(*coros)))


def run_with_timeout(coro, seconds: float):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(asyncio.wait_for(coro, timeout=seconds))
