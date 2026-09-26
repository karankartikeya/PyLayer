from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
inventory: dict[str, int] = {}


def load_inventory() -> dict[str, int]:
    return {"apple": 3, "pear": 0}


@app.on_event("startup")
def startup():
    inventory.update(load_inventory())


@app.on_event("shutdown")
def shutdown():
    inventory.clear()


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
