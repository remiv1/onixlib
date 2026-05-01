from decimal import Decimal
from .generated.v3_0 import Price as _Price
from .generated.v3_0 import ProductSupply as _ProductSupply
from .generated.v3_0 import SupplyDetail as _SupplyDetail

__all__ = ["ProductSupply", "SupplyDetail", "Price"]


class Price:
    def __init__(self, raw: _Price) -> None: ...    # pylint: disable=unused-argument

    @property
    def price_type(self) -> str: ...

    @property
    def amount(self) -> Decimal | None: ...

    @property
    def currency(self) -> str: ...

    @property
    def raw(self) -> _Price: ...

    def __repr__(self) -> str: ...


class SupplyDetail:
    def __init__(self, raw: _SupplyDetail) -> None: ...    # pylint: disable=unused-argument

    @property
    def supplier_name(self) -> str | None: ...

    @property
    def availability(self) -> str | None: ...

    @property
    def prices(self) -> list[Price]: ...

    @property
    def raw(self) -> _SupplyDetail: ...

    def __repr__(self) -> str: ...


class ProductSupply:
    def __init__(self, raw: _ProductSupply) -> None: ...    # pylint: disable=unused-argument

    @property
    def supply_details(self) -> list[SupplyDetail]: ...

    @property
    def availability(self) -> str | None: ...

    @property
    def supplier_name(self) -> str | None: ...

    @property
    def prices(self) -> list[Price]: ...

    @property
    def raw(self) -> _ProductSupply: ...

    def __repr__(self) -> str: ...
