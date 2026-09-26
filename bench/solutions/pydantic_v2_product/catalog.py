from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer

PriceStr = Annotated[Decimal, Field(gt=0), PlainSerializer(lambda v: str(v), return_type=str, when_used="json")]


class Product(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    tags: list[str] = Field(min_length=1, max_length=5)
    price: PriceStr


def parse_product(data: dict) -> Product:
    return Product.model_validate(data)


def product_json(p: Product) -> str:
    return p.model_dump_json()
