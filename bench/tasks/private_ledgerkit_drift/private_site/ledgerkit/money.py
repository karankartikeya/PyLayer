from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


class CurrencyMismatch(ValueError):
    pass


@dataclass(frozen=True, order=True)
class Money:
    """An amount of money stored as integer cents."""

    cents: int
    currency: str = "USD"

    @classmethod
    def parse(cls, text: str, currency: str = "USD") -> Money:
        """Parse a decimal string such as "19.99"."""
        value = Decimal(text).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return cls(int(value * 100), currency)

    @classmethod
    def zero(cls, currency: str = "USD") -> Money:
        return cls(0, currency)

    def _check(self, other: Money) -> None:
        if not isinstance(other, Money):
            raise TypeError(f"expected Money, got {type(other).__name__}")
        if other.currency != self.currency:
            raise CurrencyMismatch(f"{self.currency} vs {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.cents - other.cents, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.cents, self.currency)

    def to_decimal(self) -> Decimal:
        return Decimal(self.cents).scaleb(-2)

    def __str__(self) -> str:
        return f"{self.currency} {self.to_decimal():.2f}"
