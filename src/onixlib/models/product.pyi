from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from .collateral import CollateralDetail
from .contributor import Contributor, ContributorRole
from .descriptive import DescriptiveDetail
from .generated.v3_0 import Product as _Product
from .product_supply import ProductSupply
from .publishing import PublishingDetail
from .related_material import RelatedMaterial

__all__ = ["Product"]


class Product:
    def __init__(self, raw: _Product) -> None: ...    # pylint: disable=unused-argument

    @classmethod
    def new(
        cls,
        isbn: str | None = None,    # pylint: disable=unused-argument
        title: str | None = None,    # pylint: disable=unused-argument
        product_form: str = "BC",    # pylint: disable=unused-argument
        product_composition: str = "00",    # pylint: disable=unused-argument
    ) -> "Product": ...

    @property
    def isbn(self) -> str | None: ...

    @isbn.setter
    def isbn(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def title(self) -> str: ...

    @title.setter
    def title(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def contributors(self) -> list[Contributor]: ...

    def add_contributor(self, role: ContributorRole = ContributorRole.A01) -> Contributor: ...    # pylint: disable=unused-argument

    @property
    def author(self) -> Contributor | None: ...

    @property
    def authors(self) -> Optional[list[Contributor]]: ...

    @dataclass(frozen=True)
    class Editor:
        gln: str | None
        name: str | None

    @dataclass(frozen=True)
    class Publisher:
        gln: str | None
        name: str | None

    @dataclass(frozen=True)
    class Price:
        ht: Decimal | None
        ttc: Decimal | None
        currency: str | None
        vat_rate: Decimal | None

    @property
    def editor(self) -> Editor | None: ...

    @property
    def publisher(self) -> Publisher | None: ...

    @property
    def price(self) -> Price | None: ...

    @property
    def descriptive(self) -> DescriptiveDetail | None: ...

    @property
    def collateral(self) -> CollateralDetail | None: ...

    @property
    def publishing(self) -> PublishingDetail | None: ...

    @property
    def product_supply(self) -> list[ProductSupply]: ...

    @property
    def related_material(self) -> RelatedMaterial | None: ...

    def to_xml(self) -> str: ...

    @property
    def raw(self) -> _Product: ...

    def __repr__(self) -> str: ...
