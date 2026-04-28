"""Facade for the ONIX 3.0 ProductSupply block."""

from __future__ import annotations

from decimal import Decimal

from .generated.v3_0 import (
    Price as _Price,
    ProductSupply as _ProductSupply,
    SupplyDetail as _SupplyDetail,
)

__all__ = ["ProductSupply", "SupplyDetail", "Price"]


class Price:
    """Lightweight facade over one ONIX ``<Price>`` element."""

    def __init__(self, raw: _Price) -> None:
        self._raw = raw

    @property
    def price_type(self) -> str:
        """Price type code (List 58), e.g. ``"02"`` = RRP excluding tax."""
        return self._raw.price_type.value.value if self._raw.price_type else ""

    @property
    def amount(self) -> Decimal | None:
        """Price amount as :class:`~decimal.Decimal`, or ``None`` if absent."""
        if self._raw.price_amount is None:
            return None
        return Decimal(str(self._raw.price_amount.value))

    @property
    def currency(self) -> str:
        """ISO 4217 currency code (List 96), e.g. ``"EUR"``."""
        return self._raw.currency_code.value.value if self._raw.currency_code else ""

    @property
    def raw(self) -> _Price:
        """Returns the underlying xsdata ``Price`` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        r = f"Price(type={self.price_type!r}, amount={self.amount!r}, currency={self.currency!r})"
        return r


class SupplyDetail:
    """Lightweight facade over one ONIX ``<SupplyDetail>`` element."""

    def __init__(self, raw: _SupplyDetail) -> None:
        self._raw = raw

    @property
    def supplier_name(self) -> str | None:
        """Name of the supplier, or ``None`` if absent."""
        return self._raw.supplier.supplier_name.value if self._raw.supplier.supplier_name else None

    @property
    def availability(self) -> str | None:
        """Product availability code (List 65), or ``None`` if absent.

        Common values: ``"20"`` = available, ``"40"`` = not yet available.
        """
        return self._raw.product_availability.value.value

    @property
    def prices(self) -> list[Price]:
        """All prices for this supply detail."""
        return [Price(p) for p in self._raw.price]

    @property
    def raw(self) -> _SupplyDetail:
        """Returns the underlying xsdata ``SupplyDetail`` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"SupplyDetail(supplier={self.supplier_name!r}, availability={self.availability!r})"


class ProductSupply:
    """Ergonomic facade over the ONIX :class:`ProductSupply` dataclass."""

    def __init__(self, raw: _ProductSupply) -> None:
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Supply details                                                       #
    # ------------------------------------------------------------------ #

    @property
    def supply_details(self) -> list[SupplyDetail]:
        """All supply details within this ProductSupply block."""
        return [SupplyDetail(sd) for sd in self._raw.supply_detail]

    @property
    def availability(self) -> str | None:
        """Availability code from the first supply detail, or ``None``."""
        for sd in self._raw.supply_detail:
            if sd.product_availability:
                return sd.product_availability.value.value
        return None

    @property
    def supplier_name(self) -> str | None:
        """Supplier name from the first supply detail, or ``None``."""
        for sd in self._raw.supply_detail:
            if sd.supplier and sd.supplier.supplier_name:
                return sd.supplier.supplier_name.value
        return None

    @property
    def prices(self) -> list[Price]:
        """All prices across all supply details, flattened."""
        result: list[Price] = []
        for sd in self._raw.supply_detail:
            result.extend(Price(p) for p in sd.price)
        return result

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _ProductSupply:
        """Returns the underlying xsdata :class:`ProductSupply` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return (
            f"ProductSupply("
            f"supplier={self.supplier_name!r}, "
            f"availability={self.availability!r}, "
            f"prices={len(self.prices)})"
        )
