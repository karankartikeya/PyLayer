import httpx


def make_client(base_url: str, proxy_url: str | None = None, timeout: float = 5.0) -> httpx.Client:
    proxies = {"all://": proxy_url} if proxy_url else None
    return httpx.Client(base_url=base_url, proxies=proxies, timeout=timeout)


async def fetch_json(app, path: str) -> dict:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(path)
        response.raise_for_status()
        return response.json()
