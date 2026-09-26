import asyncio


def run_all(coros: list) -> list:
    async def main():
        return await asyncio.gather(*coros)

    return list(asyncio.run(main()))


def run_with_timeout(coro, seconds: float):
    return asyncio.run(asyncio.wait_for(coro, timeout=seconds))
