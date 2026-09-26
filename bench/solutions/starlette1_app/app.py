from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


def open_store() -> dict:
    return {"hits": 0}


def close_store(store: dict) -> None:
    store["closed"] = True


@asynccontextmanager
async def lifespan(app: Starlette):
    app.state.store = open_store()
    try:
        yield
    finally:
        close_store(app.state.store)


async def hit(request: Request) -> JSONResponse:
    store = request.app.state.store
    store["hits"] += 1
    return JSONResponse({"hits": store["hits"]})


async def boom(request: Request):
    raise KeyError("boom")


async def key_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"error": "not found"}, status_code=404)


app = Starlette(
    routes=[Route("/hit", hit), Route("/boom", boom)],
    exception_handlers={KeyError: key_error_handler},
    lifespan=lifespan,
)
