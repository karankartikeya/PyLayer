import httpx


def make_client(base_url: str, proxy_url: str | None = None, timeout: float = 5.0) -> httpx.Client:
    return httpx.Client(base_url=base_url, proxy=proxy_url, timeout=timeout)


async def fetch_json(app, path: str) -> dict:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(path)
        response.raise_for_status()
        return response.json()
