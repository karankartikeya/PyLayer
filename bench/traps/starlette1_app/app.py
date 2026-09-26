from starlette.applications import Starlette
from starlette.responses import JSONResponse

store: dict = {}


def open_store() -> dict:
    return {"hits": 0}


def close_store(store: dict) -> None:
    store["closed"] = True


def startup():
    store.update(open_store())


def shutdown():
    close_store(store)


app = Starlette(on_startup=[startup], on_shutdown=[shutdown])


@app.route("/hit")
async def hit(request):
    store["hits"] += 1
    return JSONResponse({"hits": store["hits"]})


@app.route("/boom")
async def boom(request):
    raise KeyError("boom")


@app.exception_handler(KeyError)
async def key_error_handler(request, exc):
    return JSONResponse({"error": "not found"}, status_code=404)
