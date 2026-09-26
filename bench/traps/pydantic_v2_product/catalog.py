from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel):
    sku: str = Field(regex=r"^[A-Z]{3}-\d{4}$")
    tags: list[str] = Field(min_items=1, max_items=5)
    price: Decimal = Field(gt=0)

    class Config:
        json_encoders = {Decimal: str}


def parse_product(data: dict) -> Product:
    return Product.parse_obj(data)


def product_json(p: Product) -> str:
    return p.json()
