from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

inventory: dict[str, int] = {}


def load_inventory() -> dict[str, int]:
    return {"apple": 3, "pear": 0}


@asynccontextmanager
async def lifespan(app: FastAPI):
    inventory.update(load_inventory())
    yield
    inventory.clear()


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str
    quantity: int


@app.get("/items/{name}", response_model=Item)
def get_item(name: str) -> Item:
    if name not in inventory:
        raise HTTPException(status_code=404, detail="item not found")
    return Item(name=name, quantity=inventory[name])


@app.get("/items")
def list_items(in_stock: bool = False) -> list[str]:
    return [n for n, q in inventory.items() if not in_stock or q > 0]
