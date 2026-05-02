"""Facade for the ONIX 3.0 Product block.

This is the central facade: it wraps the xsdata-generated
:class:`~onixlib.models.generated.v3_0.Product` dataclass and composes the
per-block facades (:class:`~onixlib.models.descriptive.DescriptiveDetail`,
:class:`~onixlib.models.collateral.CollateralDetail`, etc.).

Example usage::

    from onixlib import parse

    for product in parse("notice.xml"):
        print(product.isbn, product.title)
        for c in product.contributors:
            print(c.role, c.full_name)
        print(product.collateral.description)
        print(product.publishing.publication_date)
        for ps in product.product_supply:
            for price in ps.prices:
                print(price.amount, price.currency)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from typing import Optional

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .collateral import CollateralDetail
from .contributor import Contributor, ContributorRole
from .descriptive import DescriptiveDetail
from .generated.v3_0 import (
    DescriptiveDetail as _DescriptiveDetail,
    Idvalue,
    List1,
    List2,
    List5,
    List150,
    NotificationType,
    Price as _RawPrice,
    Product as _Product,
    ProductComposition,
    ProductForm,
    ProductIdentifier,
    ProductIdtype,
    RecordReference,
)
from .product_supply import ProductSupply
from .publishing import PublishingDetail
from .related_material import RelatedMaterial

__all__ = ["Product"]

_ISBN13_TYPE = List5.VALUE_15  # "15" – ISBN-13
_GTIN13_TYPE = List5.VALUE_03  # "03" – GTIN-13
_PUBLISHER_GLN_TYPE = "06"  # List 44 code for GLN in PublisherIdentifier
_PRICE_TYPE_HT = "01"  # RRP excluding tax
_PRICE_TYPE_TTC = "04"  # RRP including tax

_context = XmlContext()
_serializer = XmlSerializer(
    context=_context,
    config=SerializerConfig(indent="  ", xml_declaration=True),
)


class Product:
    """Ergonomic facade over the ONIX :class:`Product` dataclass."""

    def __init__(self, raw: _Product) -> None:
        self._raw = raw
        self._descriptive: DescriptiveDetail | None = None
        self._collateral: CollateralDetail | None = None
        self._publishing: PublishingDetail | None = None
        self._related_material: RelatedMaterial | None = None

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def new(
        cls,
        isbn: str | None = None,
        title: str | None = None,
        product_form: str = "BC",
        product_composition: str = "00",
    ) -> "Product":
        """Create a new Product with sensible defaults.

        Args:
            isbn:                ISBN-13 (no dashes).
            title:               Main title.
            product_form:        ONIX List 150 code, e.g. ``"BC"`` (paperback),
                                 ``"BB"`` (hardback).
            product_composition: ONIX List 2 code, e.g. ``"00"`` (single-component).
        """
        pf_enum = List150(product_form)
        pc_enum = List2(product_composition)
        descriptive = _DescriptiveDetail(
            product_composition=ProductComposition(value=pc_enum),
            product_form=ProductForm(value=pf_enum),
        )
        raw = _Product(
            record_reference=RecordReference(value=isbn or ""),
            notification_type=NotificationType(value=List1.VALUE_03),
            product_identifier=[],
            descriptive_detail=descriptive,
        )
        product = cls(raw)
        if isbn:
            product.isbn = isbn
        if title:
            product.title = title
        return product

    # ------------------------------------------------------------------ #
    # Identifier                                                           #
    # ------------------------------------------------------------------ #

    @property
    def isbn(self) -> str | None:
        """ISBN-13 (or GTIN-13) of the product, or ``None`` if absent."""
        for pi in self._raw.product_identifier:
            if pi.product_idtype.value in (_ISBN13_TYPE, _GTIN13_TYPE):
                return pi.idvalue.value
        return None

    @isbn.setter
    def isbn(self, value: str) -> None:
        for pi in self._raw.product_identifier:
            if pi.product_idtype.value == _ISBN13_TYPE:
                pi.idvalue.value = value
                return
        self._raw.product_identifier.append(
            ProductIdentifier(
                product_idtype=ProductIdtype(value=_ISBN13_TYPE),
                idvalue=Idvalue(value=value),
            )
        )

    # ------------------------------------------------------------------ #
    # Title / author shortcuts (delegate to descriptive)                  #
    # ------------------------------------------------------------------ #

    @property
    def title(self) -> str:
        """Main title of the product. Delegates to :attr:`descriptive`."""
        return self.descriptive.title if self.descriptive else ""

    @title.setter
    def title(self, value: str) -> None:
        if self.descriptive is None:
            raise AttributeError(
                "This product has no DescriptiveDetail. "
                "Use Product.new() or initialise raw.descriptive_detail first."
            )
        self.descriptive.title = value

    @property
    def contributors(self) -> list[Contributor]:
        """All contributors. Delegates to :attr:`descriptive`."""
        return self.descriptive.contributors if self.descriptive else []

    def add_contributor(self, role: ContributorRole = ContributorRole.A01) -> Contributor:
        """Append a contributor. Delegates to :attr:`descriptive`.

        Args:
            role: ONIX contributor role (``List17`` enum). Defaults to ``A01``.
        """
        if self.descriptive is None:
            raise AttributeError(
                "This product has no DescriptiveDetail. "
                "Use Product.new() or initialise raw.descriptive_detail first."
            )
        return self.descriptive.add_contributor(role)

    @property
    def authors(self) -> Optional[list[Contributor]]:
        """
        List of contributor with role ``A01`` (written by) or ``A02`` (co-written by).
        Delegates to :attr:`descriptive`.
        """
        authors = [
            c for c in self.contributors if c.role in (ContributorRole.A01, ContributorRole.A02)
        ]
        return authors if authors else None

    @property
    def author(self) -> Contributor | None:
        """First contributor with role ``A01`` (written by), or ``None``."""
        for contributor in self.contributors:
            if contributor.role == ContributorRole.A01:
                return contributor
        return None

    @dataclass(frozen=True)
    class Editor:
        """Editor facade extracted from the first ``<Publisher>`` block."""

        gln: str | None
        name: str | None

    @dataclass(frozen=True)
    class Price:
        """Aggregated product price fields derived from ``<SupplyDetail>`` prices."""

        ht: Decimal | None
        ttc: Decimal | None
        currency: str | None
        vat_rate: Decimal | None

    @property
    def editor(self) -> Editor | None:
        """Editor facade with ``gln`` and ``name``, or ``None`` if absent."""
        publishing = self._raw.publishing_detail
        if publishing is None or not publishing.publisher:
            return None

        pub = publishing.publisher[0]
        name = pub.publisher_name.value if pub.publisher_name else None

        gln: str | None = None
        for identifier in pub.publisher_identifier:
            if identifier.publisher_idtype.value.value == _PUBLISHER_GLN_TYPE:
                gln = identifier.idvalue.value
                break

        if gln is None and name is None:
            return None
        return Product.Editor(gln=gln, name=name)

    @staticmethod
    def _iter_raw_prices(raw: _Product):
        for product_supply in raw.product_supply:
            for supply_detail in product_supply.supply_detail:
                for price in supply_detail.price:
                    yield price

    @staticmethod
    def _price_type(price: _RawPrice) -> str:
        return price.price_type.value.value if price.price_type else ""

    @staticmethod
    def _price_amount(price: _RawPrice) -> Decimal | None:
        if price.price_amount is None:
            return None
        return Decimal(str(price.price_amount.value))

    @staticmethod
    def _price_currency(price: _RawPrice) -> str | None:
        return price.currency_code.value.value if price.currency_code else None

    @staticmethod
    def _price_vat_rate(price: _RawPrice) -> Decimal | None:
        for tax in price.tax:
            if tax.tax_rate_percent is not None:
                return Decimal(str(tax.tax_rate_percent.value))
        return None

    @staticmethod
    def _first_price_by_type(prices: list[_RawPrice], price_type: str) -> _RawPrice | None:
        for price in prices:
            if Product._price_type(price) == price_type:
                return price
        return None

    @staticmethod
    def _first_price_currency(prices: list[_RawPrice]) -> str | None:
        for price in prices:
            currency = Product._price_currency(price)
            if currency is not None:
                return currency
        return None

    @property
    def price(self) -> Price | None:
        """Price facade with ``ht``, ``ttc``, ``currency`` and ``vat_rate`` fields."""
        prices = list(Product._iter_raw_prices(self._raw))
        if not prices:
            return None

        ht_price = Product._first_price_by_type(prices, _PRICE_TYPE_HT)
        ttc_price = Product._first_price_by_type(prices, _PRICE_TYPE_TTC)

        ht = Product._price_amount(ht_price) if ht_price else None
        ttc = Product._price_amount(ttc_price) if ttc_price else None
        currency = (
            Product._price_currency(ttc_price)
            if ttc_price is not None
            else Product._first_price_currency(prices)
        )
        vat_rate = Product._price_vat_rate(ttc_price) if ttc_price is not None else None

        if ht is None and ttc is None and currency is None and vat_rate is None:
            return None
        return Product.Price(ht=ht, ttc=ttc, currency=currency, vat_rate=vat_rate)

    # ------------------------------------------------------------------ #
    # Block facades                                                        #
    # ------------------------------------------------------------------ #

    @property
    def descriptive(self) -> DescriptiveDetail | None:
        """Facade over the ``<DescriptiveDetail>`` block, or ``None``."""
        if self._descriptive is None and self._raw.descriptive_detail is not None:
            self._descriptive = DescriptiveDetail(self._raw.descriptive_detail)
        return self._descriptive

    @property
    def collateral(self) -> CollateralDetail | None:
        """Facade over the ``<CollateralDetail>`` block, or ``None``."""
        if self._collateral is None and self._raw.collateral_detail is not None:
            self._collateral = CollateralDetail(self._raw.collateral_detail)
        return self._collateral

    @property
    def publishing(self) -> PublishingDetail | None:
        """Facade over the ``<PublishingDetail>`` block, or ``None``."""
        if self._publishing is None and self._raw.publishing_detail is not None:
            self._publishing = PublishingDetail(self._raw.publishing_detail)
        return self._publishing

    @property
    def product_supply(self) -> list[ProductSupply]:
        """List of facades over each ``<ProductSupply>`` block."""
        return [ProductSupply(ps) for ps in self._raw.product_supply]

    @property
    def related_material(self) -> RelatedMaterial | None:
        """Facade over the ``<RelatedMaterial>`` block, or ``None``."""
        if self._related_material is None and self._raw.related_material is not None:
            self._related_material = RelatedMaterial(self._raw.related_material)
        return self._related_material

    # ------------------------------------------------------------------ #
    # Serialization                                                        #
    # ------------------------------------------------------------------ #

    def to_xml(self) -> str:
        """Serialize this product to an ONIX 3.0 XML string."""
        out = StringIO()
        _serializer.write(out, self._raw)  # pyright: ignore[reportUnknownMemberType]
        return out.getvalue()

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _Product:
        """Returns the underlying xsdata :class:`Product` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"Product(isbn={self.isbn!r}, title={self.title!r})"
